# 🛠️ Hands-On Coding Guide: GT Club Chatbot

## Prerequisites
- Python 3.8+ installed
- Code editor (VS Code recommended)
- Terminal/Command Prompt
- Internet connection

---

## Step 1: Project Setup (10 minutes)

### 1.1 Create Project Directory
```bash
mkdir gt_chatbot_workshop
cd gt_chatbot_workshop
```

### 1.2 Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate
```

### 1.3 Install Dependencies
```bash
pip install flask pymongo python-dotenv pandas google-generativeai
```

### 1.4 Create Project Structure
```bash
mkdir templates
touch hello.py
touch .env
touch sample_clubs.csv
touch upload_clubs.py
```

---

## Step 2: Basic Flask App (15 minutes)

### 2.1 Create Basic Flask Application
Create `hello.py`:

```python
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return jsonify({"message": "Hello from Flask!", "status": "success"})

if __name__ == '__main__':
    app.run(debug=True, port=8001)
```

### 2.2 Create Basic HTML Template
Create `templates/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GT Club Chatbot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .test-section {
            margin: 20px 0;
            padding: 15px;
            background: #e8f4fd;
            border-radius: 5px;
        }
        button {
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
        }
        button:hover {
            background: #0056b3;
        }
        #result {
            margin-top: 10px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid #007bff;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>GT Club Chatbot</h1>
        
        <div class="test-section">
            <h3>Test Flask Connection</h3>
            <button onclick="testConnection()">Test API</button>
            <div id="result"></div>
        </div>
    </div>

    <script>
        async function testConnection() {
            try {
                const response = await fetch('/test');
                const data = await response.json();
                document.getElementById('result').innerHTML = 
                    `<strong>Success!</strong> ${data.message}`;
            } catch (error) {
                document.getElementById('result').innerHTML = 
                    `<strong>Error:</strong> ${error.message}`;
            }
        }
    </script>
</body>
</html>
```

### 2.3 Test Your Flask App
```bash
python hello.py
```

Open your browser and go to `http://localhost:8001`

**Expected Result:** You should see a page with a "Test API" button that returns a success message.

---

## Step 3: Environment Variables (5 minutes)

### 3.1 Create .env File
Create `.env`:

```bash
MONGODB_CLIENT=mongodb://localhost:27017/
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3.2 Update hello.py to Load Environment Variables
Add to the top of `hello.py`:

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
```

### 3.3 Test Environment Variables
Add this route to test:

```python
@app.route('/env-test')
def env_test():
    return jsonify({
        "mongodb_client": os.getenv('MONGODB_CLIENT'),
        "gemini_key_set": bool(os.getenv('GEMINI_API_KEY'))
    })
```

---

## Step 4: Database Integration (20 minutes)

### 4.1 Install MongoDB
**On macOS:**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**On Windows:**
Download from [MongoDB Community Server](https://www.mongodb.com/try/download/community)

**On Ubuntu:**
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
```

### 4.2 Create Sample Data
Create `sample_clubs.csv`:

```csv
club_name,link,description,majors
Computer Science Club,https://example.com/cs-club,A club for CS students to collaborate and learn,Computer Science
Film Club,https://example.com/film-club,A welcoming community for creativity,Finance Economics
Robotics Club,https://example.com/robotics,Building robots and competing in competitions,Engineering
```

### 4.3 Create Data Upload Script
Create `upload_clubs.py`:

```python
import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to MongoDB
client = MongoClient(os.getenv('MONGODB_CLIENT'), tlsAllowInvalidCertificates=True)
db = client["files"]
collection = db["clubs"]

# Read CSV and upload to MongoDB
df = pd.read_csv('sample_clubs.csv')
clubs_data = df.to_dict('records')

# Clear existing data and insert new data
collection.delete_many({})
collection.insert_many(clubs_data)

print(f"Uploaded {len(clubs_data)} clubs to MongoDB")

client.close()
```

### 4.4 Upload Data to MongoDB
```bash
python upload_clubs.py
```

### 4.5 Add Database Routes to Flask App
Add these routes to `hello.py`:

```python
from pymongo import MongoClient

# Database setup
client = MongoClient(os.getenv('MONGODB_CLIENT'), tlsAllowInvalidCertificates=True)
db = client["files"]
collection = db["clubs"]

@app.route('/clubs', methods=['GET'])
def get_all_clubs():
    """Get all clubs from the database"""
    try:
        clubs = list(collection.find({}, {'_id': 0}))
        return jsonify({
            'success': True,
            'clubs': clubs,
            'count': len(clubs)
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
        # Case-insensitive search
        clubs = list(collection.find(
            {"club_name": {"$regex": club_name, "$options": "i"}}, 
            {'_id': 0}
        ))
        
        if clubs:
            return jsonify({
                'success': True,
                'clubs': clubs,
                'count': len(clubs)
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
```

### 4.6 Test Database Integration
Restart your Flask app and test:

```bash
# Test getting all clubs
curl http://localhost:8001/clubs

# Test getting specific club
curl http://localhost:8001/clubs/Computer
```

---

## Step 5: AI Integration (25 minutes)

### 5.1 Get Google Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API Key"
4. Create a new API key
5. Copy the key and update your `.env` file

### 5.2 Add Gemini Integration to Flask App
Add to the top of `hello.py`:

```python
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
```

### 5.3 Create Chat Endpoint
Add this route to `hello.py`:

```python
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
        clubs_context = "\n".join([
            f"Club: {club['club_name']} - {club['description']} - Majors: {club['majors']}"
            for club in clubs[:10]  # Limit to first 10 clubs for context
        ])

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
```

### 5.4 Test AI Integration
```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What clubs are available for computer science students?"}'
```

---

## Step 6: Frontend Development (30 minutes)

### 6.1 Update HTML Template
Replace the content of `templates/index.html` with:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GT Club Chatbot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            color: #fff;
        }
        
        .chat-container {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            width: 90%;
            max-width: 600px;
            height: 80vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .chat-header {
            background-color: rgba(0, 0, 0, 0.2);
            padding: 15px;
            text-align: center;
            font-size: 1.4em;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .chat-box {
            flex-grow: 1;
            padding: 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }
        
        .message {
            margin-bottom: 10px;
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 80%;
            word-wrap: break-word;
        }
        
        .message.user {
            align-self: flex-end;
            background-color: #2575fc;
            border-bottom-right-radius: 5px;
        }
        
        .message.bot {
            align-self: flex-start;
            background-color: rgba(255, 255, 255, 0.2);
            border-bottom-left-radius: 5px;
        }
        
        .chat-input-container {
            display: flex;
            padding: 15px;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
            background-color: rgba(0, 0, 0, 0.2);
        }
        
        .chat-input-container input {
            flex-grow: 1;
            padding: 10px 15px;
            border: none;
            border-radius: 20px;
            background-color: rgba(255, 255, 255, 0.9);
            color: #333;
            font-size: 1em;
            margin-right: 10px;
        }
        
        .chat-input-container input:focus {
            outline: none;
            box-shadow: 0 0 0 2px #6a11cb;
        }
        
        .chat-input-container button {
            background-color: #6a11cb;
            color: white;
            border: none;
            border-radius: 20px;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 1em;
            transition: background-color 0.3s ease;
        }
        
        .chat-input-container button:hover {
            background-color: #5a0ea0;
        }
        
        .loading-indicator {
            align-self: flex-start;
            margin-top: 5px;
            font-style: italic;
            color: rgba(255, 255, 255, 0.7);
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            GT Club Chatbot
        </div>
        <div class="chat-box" id="chat-box">
            <div class="message bot">Hello! I'm your GT Club Chatbot. How can I help you find a club today?</div>
        </div>
        <div class="chat-input-container">
            <input type="text" id="user-input" placeholder="Type your message...">
            <button id="send-button">Send</button>
        </div>
    </div>

    <script>
        const chatBox = document.getElementById('chat-box');
        const userInput = document.getElementById('user-input');
        const sendButton = document.getElementById('send-button');

        sendButton.addEventListener('click', sendMessage);
        userInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        async function sendMessage() {
            const message = userInput.value.trim();
            if (message === '') return;

            appendMessage(message, 'user');
            userInput.value = '';

            const loadingDiv = document.createElement('div');
            loadingDiv.classList.add('message', 'bot', 'loading-indicator');
            loadingDiv.textContent = 'Typing...';
            chatBox.appendChild(loadingDiv);
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();

                chatBox.removeChild(loadingDiv);

                if (data.success) {
                    appendMessage(data.response, 'bot');
                } else {
                    appendMessage(`Error: ${data.error}`, 'bot');
                }
            } catch (error) {
                chatBox.removeChild(loadingDiv);
                appendMessage(`Error connecting to the server: ${error}`, 'bot');
            }
        }

        function appendMessage(message, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message', sender);
            messageDiv.textContent = message;
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>
```

### 6.2 Test the Complete Application
1. Restart your Flask app
2. Open `http://localhost:8001` in your browser
3. Try asking questions like:
   - "What clubs are available?"
   - "Tell me about the Computer Science Club"
   - "I'm interested in robotics, what clubs do you recommend?"

---

## Step 7: Testing and Debugging (15 minutes)

### 7.1 Test All Endpoints
```bash
# Test home page
curl http://localhost:8001/

# Test clubs endpoint
curl http://localhost:8001/clubs

# Test specific club
curl http://localhost:8001/clubs/Computer

# Test chat endpoint
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

### 7.2 Common Issues and Solutions

**Issue: MongoDB connection error**
```bash
# Check if MongoDB is running
brew services list | grep mongodb
# or
sudo systemctl status mongod
```

**Issue: Gemini API error**
- Check your API key in `.env`
- Verify the key is correct
- Check if you have credits remaining

**Issue: CORS errors**
- Make sure you're using the correct URL
- Check if Flask is running on the right port

### 7.3 Add Error Logging
Add this to your Flask app for better debugging:

```python
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add logging to your routes
@app.route('/chat', methods=['POST'])
def chat():
    try:
        logger.info(f"Received chat request: {request.get_json()}")
        # ... rest of your code
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        # ... error handling
```

---

## Step 8: Enhancements (Optional - 20 minutes)

### 8.1 Add More Club Data
Create a more comprehensive `sample_clubs.csv`:

```csv
club_name,link,description,majors
Computer Science Club,https://example.com/cs-club,A club for CS students to collaborate and learn,Computer Science
Film Club,https://example.com/film-club,A welcoming community for creativity,Finance Economics
Robotics Club,https://example.com/robotics,Building robots and competing in competitions,Engineering
Debate Society,https://example.com/debate,Improving public speaking and critical thinking,Philosophy Political Science
Photography Club,https://example.com/photo,Capturing moments and learning techniques,Art Design
Entrepreneurship Hub,https://example.com/entrepreneur,Supporting student startups and innovation,Business Economics
Environmental Club,https://example.com/environment,Promoting sustainability and green initiatives,Environmental Science
Music Society,https://example.com/music,Creating and performing music together,Music Arts
```

### 8.2 Add More API Endpoints
```python
@app.route('/clubs', methods=['POST'])
def create_club():
    """Create a new club"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['club_name', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Insert new club
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
    """Update an existing club"""
    try:
        data = request.get_json()
        
        # Update club
        result = collection.update_one(
            {"club_name": {"$regex": club_name, "$options": "i"}},
            {"$set": data}
        )
        
        if result.matched_count == 0:
            return jsonify({
                'success': False,
                'error': 'Club not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Club updated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/clubs/<club_name>', methods=['DELETE'])
def delete_club(club_name):
    """Delete a club"""
    try:
        result = collection.delete_one(
            {"club_name": {"$regex": club_name, "$options": "i"}}
        )
        
        if result.deleted_count == 0:
            return jsonify({
                'success': False,
                'error': 'Club not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Club deleted successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

### 8.3 Add Input Validation
```python
def validate_club_data(data):
    """Validate club data"""
    errors = []
    
    if 'club_name' in data and len(data['club_name'].strip()) == 0:
        errors.append('Club name cannot be empty')
    
    if 'description' in data and len(data['description'].strip()) == 0:
        errors.append('Description cannot be empty')
    
    return errors
```

---

## Step 9: Final Testing (10 minutes)

### 9.1 Complete API Test Suite
```bash
#!/bin/bash
# test_api.sh

echo "Testing GT Club Chatbot API..."

echo "1. Testing home page..."
curl -s http://localhost:8001/ | head -5

echo -e "\n2. Testing clubs endpoint..."
curl -s http://localhost:8001/clubs | jq '.count'

echo -e "\n3. Testing specific club search..."
curl -s "http://localhost:8001/clubs/Computer" | jq '.clubs[0].club_name'

echo -e "\n4. Testing chat endpoint..."
curl -s -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What clubs are available?"}' | jq '.success'

echo -e "\nAll tests completed!"
```

### 9.2 Performance Testing
```python
# Add this to test performance
import time

@app.route('/performance-test')
def performance_test():
    start_time = time.time()
    
    # Test database query
    clubs = list(collection.find({}, {'_id': 0}))
    db_time = time.time() - start_time
    
    # Test AI call
    ai_start = time.time()
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Test message")
    ai_time = time.time() - ai_start
    
    return jsonify({
        'database_query_time': f"{db_time:.3f}s",
        'ai_response_time': f"{ai_time:.3f}s",
        'total_clubs': len(clubs)
    })
```

---

## Step 10: Deployment Preparation (10 minutes)

### 10.1 Create Requirements File
```bash
pip freeze > requirements.txt
```

### 10.2 Create .gitignore
Create `.gitignore`:

```gitignore
.venv/
.env
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.idea/
.vscode/
*.log
```

### 10.3 Create README
Create `README.md`:

```markdown
# GT Club Chatbot

A Flask-based web application that helps Georgia Tech students find clubs using AI.

## Features
- REST API for club management
- MongoDB database integration
- Google Gemini AI integration
- Modern responsive frontend

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables in `.env`
3. Start MongoDB
4. Run: `python hello.py`

## API Endpoints
- `GET /clubs` - Get all clubs
- `POST /clubs` - Create new club
- `GET /clubs/<name>` - Search clubs
- `POST /chat` - Chat with AI

## Technologies
- Flask (Python web framework)
- MongoDB (NoSQL database)
- Google Gemini (AI)
- HTML/CSS/JavaScript (Frontend)
```

---

## 🎉 Congratulations!

You've successfully built a complete web application with:
- ✅ REST API backend
- ✅ Database integration
- ✅ AI integration
- ✅ Modern frontend
- ✅ Error handling
- ✅ Testing

## Next Steps
1. Deploy to cloud (Heroku, AWS, etc.)
2. Add user authentication
3. Implement real-time features
4. Add more AI capabilities
5. Create mobile app

## Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Google Gemini API](https://ai.google.dev/docs)
- [JavaScript MDN](https://developer.mozilla.org/)

Happy coding! 🚀
