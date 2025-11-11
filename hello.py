from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from functools import wraps
import pandas as pd
import os
from dotenv import load_dotenv
import google.generativeai as genai
import jwt
from datetime import datetime, timedelta
import time, uuid, hashlib   # <-- added for session + memory

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')

# MongoDB connection with error handling
try:
    mongodb_client = os.getenv('MONGODB_CLIENT')
    if not mongodb_client or mongodb_client == 'your_mongodb_connection_string_here':
        raise ValueError("MONGODB_CLIENT not set in .env file")
    client = MongoClient(mongodb_client, tlsAllowInvalidCertificates=True)
    db = client["files"]
    collection = db["clubs"]
    users_collection = db['users']  # For authentication
    sessions_collection = db['sessions']   # new for chat memory
    messages_collection = db['messages']   # new for chat memory
    # create indexes for speed (optional safe)
    sessions_collection.create_index([("user_id", 1), ("updated_at", -1)])
    messages_collection.create_index([("user_id", 1), ("session_id", 1), ("ts", 1)])
    print("✓ MongoDB connection successful")
except Exception as e:
    print(f"✗ MongoDB connection error: {e}")
    raise

# Configure Gemini API with error handling
gemini_key = os.getenv('GEMINI_API_KEY')
if gemini_key and gemini_key != 'your_gemini_api_key_here':
    try:
        genai.configure(api_key=gemini_key)
        print("✓ Gemini API configured")
        GEMINI_AVAILABLE = True
    except Exception as e:
        print(f"⚠ Gemini API configuration error: {e}")
        print("⚠ Chat feature may not work without valid Gemini API key")
        GEMINI_AVAILABLE = False
else:
    print("⚠ Gemini API key not set - chat feature will not work")
    GEMINI_AVAILABLE = False


# ================== MEMORY UTILITIES (new section) ==================
def get_user_id():
    """generate stable id from ip+ua or jwt"""
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        try:
            data = jwt.decode(token[7:], app.config['SECRET_KEY'], algorithms=['HS256'])
            return f"email:{data['email']}"
        except Exception:
            pass
    raw = (request.remote_addr or '') + (request.user_agent.string or '')
    return "anon:" + hashlib.sha256(raw.encode()).hexdigest()[:32]

def get_or_create_default_session(user_id):
    """create a default chat session per user if not exists"""
    sid = "default"
    doc = sessions_collection.find_one({"user_id": user_id, "session_id": sid})
    if not doc:
        sessions_collection.insert_one({
            "user_id": user_id,
            "session_id": sid,
            "title": "Default chat",
            "created_at": time.time(),
            "updated_at": time.time()
        })
    return sid
# ===============================================================


# ============= AUTHENTICATION SECTION =============

def token_required(f):
    """Decorator to protect routes with JWT authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            
            # Decode and verify JWT token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = users_collection.find_one({'email': data['email']}, {'_id': 0, 'password': 0})
            
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

@app.route('/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        
        if not email or not password or not name:
            return jsonify({'error': 'Email, password, and name are required'}), 400
        
        # Check if user exists
        if users_collection.find_one({'email': email}):
            return jsonify({'error': 'User already exists'}), 400
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create user document
        user = {
            'email': email,
            'password': hashed_password,
            'name': name,
            'created_at': datetime.utcnow(),
            'favorite_clubs': []
        }
        
        # Insert user
        users_collection.insert_one(user)
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user': {'email': email, 'name': name}
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auth/login', methods=['POST'])
def login():
    """Login and get JWT token"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user in database
        user = users_collection.find_one({'email': email})
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Generate JWT token
        token = jwt.encode({
            'email': email,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'email': user['email'],
                'name': user['name']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auth/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """Get current user profile (protected route example)"""
    return jsonify({
        'success': True,
        'user': current_user
    }), 200

# ============= CLUB ROUTES =============

@app.route('/clubs', methods=['GET'])
def get_all_clubs():
    """Get all clubs from the database"""
    try:
        clubs = list(collection.find({}, {'_id': 0}))
        return jsonify({
            'success': True,
            'count': len(clubs),
            'clubs': clubs
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/clubs/<club_name>', methods=['GET'])
def get_club_by_name(club_name):
    """Get clubs matching the name (case-insensitive)"""
    try:
        # Case-insensitive search using regex
        clubs = list(collection.find(
            {'club_name': {'$regex': club_name, '$options': 'i'}}, 
            {'_id': 0}
        ))
        return jsonify({
            'success': True,
            'count': len(clubs),
            'clubs': clubs
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/clubs', methods=['POST'])
def create_club():
    """Create a new club"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['club_name', 'link', 'description', 'majors']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Insert the new club
        result = collection.insert_one(data)
        
        return jsonify({
            'success': True,
            'message': 'Club created successfully',
            'club_id': str(result.inserted_id)
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/clubs/<club_name>', methods=['PUT'])
def update_club(club_name):
    """Update a club by name"""
    try:
        data = request.get_json()
        
        # Remove _id if present to avoid conflicts
        if '_id' in data:
            del data['_id']
        
        # Update the club (case-insensitive search)
        result = collection.update_many(
            {'club_name': {'$regex': club_name, '$options': 'i'}},
            {'$set': data}
        )
        
        if result.modified_count > 0:
            return jsonify({
                'success': True,
                'message': f'Updated {result.modified_count} club(s)',
                'modified_count': result.modified_count
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No clubs found with that name'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/clubs/<club_name>', methods=['DELETE'])
def delete_club(club_name):
    """Delete clubs by name (case-insensitive)"""
    try:
        # Delete clubs matching the name (case-insensitive)
        result = collection.delete_many(
            {'club_name': {'$regex': club_name, '$options': 'i'}}
        )
        
        if result.deleted_count > 0:
            return jsonify({
                'success': True,
                'message': f'Deleted {result.deleted_count} club(s)',
                'deleted_count': result.deleted_count
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No clubs found with that name'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/')
def index():
    """Serve the main chatbot UI"""
    return render_template('index.html')

# ============= CHAT ROUTE (UPDATED WITH MEMORY) =============

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages with Gemini (now stores short-term memory)"""
    try:
        # STEP 0 — sanity: Gemini must be configured
        if not GEMINI_AVAILABLE:
            return jsonify({
                'success': False,
                'error': 'Gemini API key not configured. Please set GEMINI_API_KEY in your .env file.'
            }), 400
        
        # STEP 1 — read the incoming JSON and basic validation
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
            
        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400

        # ------------------------------------------------------------------
        # STEP 2 — identify the user and pick a session (TASK → add memory key)
        # TASK: get a stable user_id and a session_id (use default if missing)
        # history depends on these two keys.
        # SOLUTION (uncomment the two lines below during the demo):
        user_id = get_user_id()
        session_id = data.get('session_id', '').strip() or get_or_create_default_session(user_id)

        # For the starter (no memory yet), keep harmless placeholders:
        user_id = "demo-user"                 # will be replaced by SOLUTION
        session_id = "demo-session"           # will be replaced by SOLUTION
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # STEP 3 — fetch last 8 turns to build short-term memory (TASK)
        # TASK: pull last 8 messages for (user_id, session_id), newest → oldest,
        #       then reverse and join into a readable conversation block.
        # SOLUTION (uncomment this block during the demo):
        history = list(messages_collection.find(
            {"user_id": user_id, "session_id": session_id},
            {"_id": 0, "role": 1, "text": 1}
        ).sort("ts", -1).limit(8))
        history = list(reversed(history))
        history_text = "\n".join([f"{m['role'].title()}: {m['text']}" for m in history])

        # Starter fallback (no memory yet):
        history_text = ""                     # will be replaced by SOLUTION
        # ------------------------------------------------------------------

        # STEP 4 — get clubs for grounding (kept as-is)
        try:
            clubs = list(collection.find({}, {'_id': 0}))
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Error fetching clubs from database: {str(e)}'
            }), 500
        
        # STEP 5 — build a small catalog block for the prompt (kept as-is)
        if clubs:
            clubs_context = "\n".join([
                f"Club: {club.get('club_name', 'Unknown')} - {club.get('description', 'No description')} - Majors: {club.get('majors', 'N/A')}"
                for club in clubs[:20]
            ])
        else:
            clubs_context = "No clubs are currently in the database."

        # ------------------------------------------------------------------
        # STEP 6 — compose the prompt (TASK → add the memory block)
        # TASK: include {history_text} under “Previous conversation:”
        system_prompt = f"""You are a helpful assistant for Georgia Tech students looking for clubs to join.

Here are some available clubs at Georgia Tech:

{clubs_context}

Previous conversation:
{history_text}

Please help students find clubs that match their interests, majors, or goals."""
        # ------------------------------------------------------------------

        # STEP 7 — call Gemini (kept as-is)
        model = genai.GenerativeModel('gemini-2.0-flash')
        full_prompt = f"{system_prompt}\n\nUser: {user_message}\n\nAssistant:"
        response = model.generate_content(full_prompt)
        bot_response = getattr(response, 'text', 'I could not generate a response.')

        # ------------------------------------------------------------------
        # STEP 8 — persist both turns + touch session timestamp (TASK)
        # TASK: insert two docs into messages_collection and update sessions_collection.updated_at
        # SOLUTION (uncomment this block during the demo):
        now = time.time()
        messages_collection.insert_one({
            "user_id": user_id, "session_id": session_id, "role": "user",
            "text": user_message, "ts": now
        })
        messages_collection.insert_one({
            "user_id": user_id, "session_id": session_id, "role": "assistant",
            "text": bot_response, "ts": now + 0.001
        })
        sessions_collection.update_one(
            {"user_id": user_id, "session_id": session_id},
            {"$set": {"updated_at": now}},
            upsert=True
        )
        # ------------------------------------------------------------------

        # STEP 9 — return the response (always include session_id once enabled)
        return jsonify({
            'success': True,
            'response': bot_response,
            'session_id': session_id
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }), 500

# ------------------- API ROUTES -------------------
@app.route("/api/members_by_department", methods=["GET"])
def api_members_by_department():
    """
    Returns JSON list of department membership totals:
    [
      {"department": "CS", "members": 120},
      {"department": "EE", "members": 40},
      ...
    ]
    """
    df = get_clubs_dataframe()
    if df.empty:
        return jsonify({"error": "no data available"}), 404

    # Normalize members column to integer
    if "members" in df.columns:
        df["members"] = pd.to_numeric(df["members"], errors="coerce").fillna(0).astype(int)
    else:
        df["members"] = 0

    grouped = df.groupby("department", dropna=False)["members"].sum().reset_index()
    result = [
        {
            "department": (row["department"] if pd.notnull(row["department"]) else "Unknown"),
            "members": int(row["members"])
        }
        for _, row in grouped.iterrows()
    ]
    return jsonify(result)


@app.route("/api/events_summary", methods=["GET"])
def api_events_summary():
    """
    Returns JSON list of club attendance summary:
    [
      {"club_name": "Big Data Big Impact", "events_2024": 10, "event_attendance_2024": 480},
      ...
    ]
    """
    df = get_clubs_dataframe()
    if df.empty:
        return jsonify({"error": "no data available"}), 404

    # Ensure numeric columns exist and are integers
    for col in ["events_2024", "event_attendance_2024"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
        else:
            df[col] = 0

    rows = df[["club_name", "events_2024", "event_attendance_2024"]].to_dict(orient="records")
    return jsonify(rows)


# ------------------- DASHBOARD HTML -------------------
# This HTML is embedded in the Python file and served via render_template_string
DASHBOARD_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>GT Club Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body { font-family: Arial, sans-serif; padding: 16px; }
    canvas { max-width: 900px; margin-bottom: 28px; }
  </style>
</head>
<body>
  <h1>GT Club Dashboard</h1>
  <p>This dashboard reads data from the Flask API endpoints and renders charts with Chart.js. It is intended for review and reference.</p>

  <h3>Members by Department</h3>
  <canvas id="barChart"></canvas>

  <h3>Event attendance per club</h3>
  <canvas id="lineChart"></canvas>

<script>
async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error('Fetch failed: ' + res.status);
  return res.json();
}

async function draw() {
  try {
    const depData = await fetchJSON('/api/members_by_department');
    const labels = depData.map(d => d.department);
    const values = depData.map(d => d.members);

    new Chart(document.getElementById('barChart'), {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Members',
          data: values,
          borderWidth: 1
        }]
      },
      options: { responsive: true, plugins: { legend: { display: false } } }
    });

    const rows = await fetchJSON('/api/events_summary');
    const clubs = rows.map(r => r.club_name);
    const attendance = rows.map(r => r.event_attendance_2024);

    new Chart(document.getElementById('lineChart'), {
      type: 'line',
      data: {
        labels: clubs,
        datasets: [{ label: 'Attendance 2024', data: attendance, fill: false, tension: 0.2 }]
      },
      options: { responsive: true }
    });
  } catch (err) {
    document.body.insertAdjacentHTML('beforeend', '<p style="color:darkred">Error loading data: ' + err.message + '</p>');
  }
}

draw();
</script>
</body>
</html>
"""


@app.route("/dashboard", methods=["GET"])
def dashboard():
    """
    Serves the embedded dashboard HTML. No template files are required.
    """
    return render_template_string(DASHBOARD_HTML)
# ------------------- END OF ADDITIONS -------------------


if __name__ == '__main__':
    print("\n" + "="*50)
    print("Starting Flask Server...")
    print("="*50)
    print(f"Server running on: http://localhost:8001")
    print(f"Debug mode: ON")
    print(f"Gemini API: {'✓ Available' if GEMINI_AVAILABLE else '✗ Not configured'}")
    print("="*50 + "\n")
    app.run(debug=True, port=8001)
