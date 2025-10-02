# 🎬 Live Coding Demo Script: GT Club Chatbot

## Pre-Demo Setup (5 minutes before start)

### Checklist
- [ ] Flask app is running on port 8001
- [ ] MongoDB is running and has sample data
- [ ] Gemini API key is configured
- [ ] Browser is open to http://localhost:8001
- [ ] Terminal is ready with project directory
- [ ] VS Code is open with the project files
- [ ] Backup of working code is ready

### Quick Test
```bash
# Test that everything is working
curl http://localhost:8001/clubs | jq '.count'
curl -X POST http://localhost:8001/chat -H "Content-Type: application/json" -d '{"message": "Hello!"}' | jq '.success'
```

---

## Demo Script (45 minutes)

### Opening (2 minutes)
**"Welcome everyone! Today we're going to build a GT Club Chatbot from scratch. This is a real-world application that combines multiple technologies: Flask for the backend, MongoDB for the database, Google Gemini for AI, and modern web technologies for the frontend."**

**"Let me show you what we're going to build..."**
- Open browser to http://localhost:8001
- Show the working chatbot
- Ask it a question: "What clubs are available for computer science students?"
- Show the response

**"Now let's build this step by step!"**

---

### Part 1: Project Setup (5 minutes)

**"First, let's set up our development environment."**

```bash
# Show the project structure
ls -la
```

**"We have a clean project directory. Let's create our virtual environment and install dependencies."**

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install flask pymongo python-dotenv pandas google-generativeai
```

**"Now let's create our basic Flask application."**

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

**"Let's test our basic Flask app."**
```bash
python hello.py
```

**"Great! Now let's create a simple HTML template."**

Create `templates/index.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GT Club Chatbot</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
        #result { margin-top: 10px; padding: 10px; background: #f8f9fa; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>GT Club Chatbot</h1>
        <button onclick="testConnection()">Test API</button>
        <div id="result"></div>
    </div>
    <script>
        async function testConnection() {
            try {
                const response = await fetch('/test');
                const data = await response.json();
                document.getElementById('result').innerHTML = `<strong>Success!</strong> ${data.message}`;
            } catch (error) {
                document.getElementById('result').innerHTML = `<strong>Error:</strong> ${error.message}`;
            }
        }
    </script>
</body>
</html>
```

**"Let's test this in the browser."**
- Open http://localhost:8001
- Click "Test API" button
- Show the success message

---

### Part 2: Environment Variables (3 minutes)

**"Now let's set up our environment variables for security."**

Create `.env`:
```bash
MONGODB_CLIENT=mongodb://localhost:27017/
GEMINI_API_KEY=your_gemini_api_key_here
```

**"Let's update our Flask app to load these environment variables."**

Add to `hello.py`:
```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@app.route('/env-test')
def env_test():
    return jsonify({
        "mongodb_client": os.getenv('MONGODB_CLIENT'),
        "gemini_key_set": bool(os.getenv('GEMINI_API_KEY'))
    })
```

**"Let's test our environment variables."**
- Visit http://localhost:8001/env-test
- Show the environment variables are loaded

---

### Part 3: Database Integration (8 minutes)

**"Now let's add our database. We'll use MongoDB to store club information."**

**"First, let's create some sample data."**

Create `sample_clubs.csv`:
```csv
club_name,link,description,majors
Computer Science Club,https://example.com/cs-club,A club for CS students to collaborate and learn,Computer Science
Film Club,https://example.com/film-club,A welcoming community for creativity,Finance Economics
Robotics Club,https://example.com/robotics,Building robots and competing in competitions,Engineering
```

**"Now let's create a script to upload this data to MongoDB."**

Create `upload_clubs.py`:
```python
import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGODB_CLIENT'), tlsAllowInvalidCertificates=True)
db = client["files"]
collection = db["clubs"]

df = pd.read_csv('sample_clubs.csv')
clubs_data = df.to_dict('records')

collection.delete_many({})
collection.insert_many(clubs_data)

print(f"Uploaded {len(clubs_data)} clubs to MongoDB")
client.close()
```

**"Let's run this script to upload our data."**
```bash
python upload_clubs.py
```

**"Now let's add database routes to our Flask app."**

Add to `hello.py`:
```python
from pymongo import MongoClient

# Database setup
client = MongoClient(os.getenv('MONGODB_CLIENT'), tlsAllowInvalidCertificates=True)
db = client["files"]
collection = db["clubs"]

@app.route('/clubs', methods=['GET'])
def get_all_clubs():
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
```

**"Let's test our database integration."**
```bash
curl http://localhost:8001/clubs
```

**"Perfect! We can see our clubs data."**

---

### Part 4: AI Integration (10 minutes)

**"Now for the exciting part - let's add AI to make our chatbot intelligent!"**

**"We'll use Google's Gemini AI to power our chatbot."**

Add to `hello.py`:
```python
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
```

**"Now let's create our chat endpoint that uses AI."**

Add to `hello.py`:
```python
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400

        # Get clubs for context
        clubs = list(collection.find({}, {'_id': 0}))
        clubs_context = "\n".join([
            f"Club: {club['club_name']} - {club['description']} - Majors: {club['majors']}"
            for club in clubs
        ])

        # Create AI prompt
        system_prompt = f"""You are a helpful assistant for Georgia Tech students looking for clubs to join.

Here are some available clubs at Georgia Tech:

{clubs_context}

Please help students find clubs that match their interests, majors, or goals. Be friendly and informative."""

        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Create full prompt
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

**"Let's test our AI integration."**
```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What clubs are available for computer science students?"}'
```

**"Amazing! Our AI is working and providing intelligent responses based on our club data."**

---

### Part 5: Frontend Development (12 minutes)

**"Now let's create a beautiful frontend for our chatbot."**

**"Let's update our HTML template with a modern chat interface."**

Replace `templates/index.html` with:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GT Club Chatbot</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
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
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">GT Club Chatbot</div>
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

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();

                if (data.success) {
                    appendMessage(data.response, 'bot');
                } else {
                    appendMessage(`Error: ${data.error}`, 'bot');
                }
            } catch (error) {
                appendMessage(`Error: ${error}`, 'bot');
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

**"Let's test our complete application!"**
- Open http://localhost:8001
- Show the beautiful chat interface
- Ask a question: "What clubs are available for engineering students?"
- Show the AI response

---

### Part 6: Live Testing and Q&A (5 minutes)

**"Let's test our chatbot with different types of questions."**

**Demo questions to ask:**
1. "What clubs are available?"
2. "Tell me about the Robotics Club"
3. "I'm interested in film, what do you recommend?"
4. "What clubs are good for business students?"

**"Let's also test our API endpoints directly."**
```bash
# Test all clubs
curl http://localhost:8001/clubs | jq '.count'

# Test specific club
curl "http://localhost:8001/clubs/Robotics" | jq '.clubs[0].description'
```

**"Now let's open it up for questions!"**

---

## Troubleshooting Guide

### Common Issues During Demo

**Issue: Flask app won't start**
```bash
# Check if port is in use
lsof -i :8001
# Kill process if needed
kill -9 <PID>
```

**Issue: MongoDB connection error**
```bash
# Check if MongoDB is running
brew services list | grep mongodb
# Start if needed
brew services start mongodb-community
```

**Issue: Gemini API error**
- Check API key in .env file
- Verify key is correct
- Check if credits are available

**Issue: CORS errors**
- Make sure you're using the correct URL
- Check if Flask is running on the right port

### Backup Plans

**If MongoDB fails:**
- Use a simple Python list instead
- Show the concept without database

**If Gemini API fails:**
- Use a simple response generator
- Show the integration pattern

**If Flask fails:**
- Use a pre-built version
- Focus on explaining the concepts

---

## Demo Tips

### Before Starting
1. **Test everything** - Run through the entire demo once
2. **Have backups** - Keep working versions of each step
3. **Prepare for questions** - Know common issues and solutions
4. **Time yourself** - Practice to stay within time limits

### During Demo
1. **Explain as you go** - Don't just code, explain what you're doing
2. **Ask for questions** - Keep audience engaged
3. **Show errors** - Debugging is part of development
4. **Test frequently** - Show that each step works

### After Demo
1. **Provide resources** - Share code and documentation
2. **Answer questions** - Be available for follow-up
3. **Encourage experimentation** - Suggest next steps
4. **Collect feedback** - Improve for next time

---

## Post-Demo Follow-up

### Resources to Share
- Complete code repository
- Workshop guide and slides
- Additional learning resources
- Contact information for questions

### Next Steps for Participants
1. Try building their own version
2. Add new features
3. Deploy to the cloud
4. Share their projects

### Common Questions and Answers

**Q: How do I deploy this to production?**
A: You can use platforms like Heroku, AWS, or Google Cloud. I'll share deployment guides.

**Q: Can I use a different database?**
A: Absolutely! You can use PostgreSQL, MySQL, or any other database with appropriate drivers.

**Q: What other AI models can I use?**
A: You can use OpenAI GPT, Anthropic Claude, or other AI services with similar integration patterns.

**Q: How do I add user authentication?**
A: You can add Flask-Login or JWT tokens for user management.

---

## Success Metrics

### By the end of this demo, participants should understand:
- ✅ How to build a REST API with Flask
- ✅ How to integrate with databases
- ✅ How to use AI APIs in applications
- ✅ How to create modern web interfaces
- ✅ How to handle errors and edge cases
- ✅ How to test and debug applications

### Technical Skills Gained:
- Flask web development
- MongoDB database operations
- AI API integration
- Frontend development
- API testing and debugging
- Project structure and organization

---

*Remember: The goal is not just to show code, but to teach concepts and inspire participants to build their own projects!* 🚀
