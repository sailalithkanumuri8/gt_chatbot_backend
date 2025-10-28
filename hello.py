from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from functools import wraps
import pandas as pd
import os
from dotenv import load_dotenv
import google.generativeai as genai
import jwt
import bcrypt
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_CLIENT'), tlsAllowInvalidCertificates=True)
db = client["files"]
collection = db["clubs"]
users_collection = db['users']

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# ============= AUTHENTICATION SECTION =============

# WORKSHOP TODO: JWT Verification Decorator (5 minutes)
def token_required(f):
    """Decorator to protect routes with JWT authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            # TODO: Decode and verify JWT token
            
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
        
        # WORKSHOP TODO: Check if user exists (3 minutes)
        
        # WORKSHOP TODO: Hash password (3 minutes)
        
        # WORKSHOP TODO: Create user document (3 minutes)
        
        # WORKSHOP TODO: Insert user in our user collection (2 minutes)
        
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
        
        # WORKSHOP TODO: Find user in database (3 minutes)
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # WORKSHOP TODO: Verify password (3 minutes)
        
        # WORKSHOP TODO: Generate JWT token (5 minutes)
        
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

# ============= PROTECTED ROUTES (Require Authentication) =============

@app.route('/favorites', methods=['GET'])
@token_required
def get_favorites(current_user):
    """Get user's favorite clubs (protected route)"""
    return jsonify({
        'success': True,
        'favorites': current_user.get('favorite_clubs', [])
    }), 200

@app.route('/favorites/<club_name>', methods=['POST'])
@token_required
def add_favorite(current_user, club_name):
    """Add club to favorites (protected route)"""
    try:
        # WORKSHOP TODO: Update user's favorite clubs (5 minutes)
        
        return jsonify({
            'success': True,
            'message': f'Added {club_name} to favorites'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/favorites/<club_name>', methods=['DELETE'])
@token_required
def remove_favorite(current_user, club_name):
    """Remove club from favorites (protected route)"""
    try:
        # WORKSHOP TODO: Remove from favorites array (5 minutes)
        
        return jsonify({
            'success': True,
            'message': f'Removed {club_name} from favorites'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============= MAIN ROUTES =============

@app.route('/')
def index():
    """Serve the main chatbot UI"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages with Gemini"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400

        # Get all clubs from database for context
        clubs = list(collection.find({}, {'_id': 0}))
        
        if clubs:
            clubs_context = "\n".join([
                f"Club: {club.get('club_name', 'Unknown')} - {club.get('description', 'No description')} - Majors: {club.get('majors', 'N/A')}"
                for club in clubs[:20]  # Limit to first 20 clubs for context
            ])
        else:
            clubs_context = "No clubs are currently in the database."

        # Create system prompt with club information
        system_prompt = f"""You are a helpful assistant for Georgia Tech students looking for clubs to join.

Here are some available clubs at Georgia Tech:

{clubs_context}

Please help students find clubs that match their interests, majors, or goals. Be friendly and informative.
If a student asks about a specific club, provide details about it. If they're looking for clubs in a particular area,
suggest relevant clubs from the list above."""

        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Create the full prompt
        full_prompt = f"{system_prompt}\n\nUser: {user_message}\n\nAssistant:"
        
        # Call Gemini API
        response = model.generate_content(full_prompt)
        bot_response = response.text

        return jsonify({
            'success': True,
            'response': bot_response
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=8001)
