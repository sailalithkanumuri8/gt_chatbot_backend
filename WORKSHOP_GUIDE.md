# 🚀 API Integration Workshop: Building a GT Club Chatbot

## Workshop Overview
**Duration:** 2-3 hours  
**Level:** Beginner to Intermediate  
**Prerequisites:** Basic Python knowledge, understanding of web concepts

---

## 📋 Table of Contents
1. [Introduction to APIs](#introduction-to-apis)
2. [Project Architecture](#project-architecture)
3. [Backend Development with Flask](#backend-development-with-flask)
4. [Database Integration with MongoDB](#database-integration-with-mongodb)
5. [AI Integration with Google Gemini](#ai-integration-with-google-gemini)
6. [Frontend Development](#frontend-development)
7. [Hands-on Coding Session](#hands-on-coding-session)
8. [Deployment and Best Practices](#deployment-and-best-practices)

---

## 1. Introduction to APIs

### What is an API?
- **API** = Application Programming Interface
- A way for different software applications to communicate
- Like a waiter in a restaurant - takes your order and brings food from kitchen

### Types of APIs
- **REST APIs** (what we're building)
- **GraphQL APIs**
- **WebSocket APIs**
- **Third-party APIs** (Google, OpenAI, etc.)

### HTTP Methods
```
GET    - Retrieve data
POST   - Create new data
PUT    - Update existing data
DELETE - Remove data
```

---

## 2. Project Architecture

### Our GT Club Chatbot Stack
```
Frontend (HTML/CSS/JS) 
    ↕ HTTP Requests
Backend (Flask/Python)
    ↕ Database Queries
Database (MongoDB)
    ↕ API Calls
AI Service (Google Gemini)
```

### Key Components
1. **Flask Backend** - Handles requests and business logic
2. **MongoDB** - Stores club data
3. **Google Gemini** - Provides AI responses
4. **HTML/CSS/JS Frontend** - User interface

---

## 3. Backend Development with Flask

### Setting Up Flask
```python
from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

app = Flask(__name__)
```

### Environment Variables (.env file)
```bash
MONGODB_CLIENT=mongodb://localhost:27017/
GEMINI_API_KEY=your_api_key_here
```

### API Endpoints Structure
```python
# GET /clubs - Get all clubs
@app.route('/clubs', methods=['GET'])
def get_all_clubs():
    # Implementation here

# POST /clubs - Create new club
@app.route('/clubs', methods=['POST'])
def create_club():
    # Implementation here

# POST /chat - Chat with AI
@app.route('/chat', methods=['POST'])
def chat():
    # Implementation here
```

---

## 4. Database Integration with MongoDB

### Why MongoDB?
- **NoSQL** database - flexible schema
- **JSON-like documents** - easy to work with
- **Scalable** - handles large datasets
- **Perfect for** - storing club information

### Connecting to MongoDB
```python
# Connect to MongoDB
client = MongoClient(os.getenv('MONGODB_CLIENT'), tlsAllowInvalidCertificates=True)
db = client["files"]
collection = db["clubs"]
```

### Sample Data Structure
```json
{
  "club_name": "Film Club",
  "link": "https://universityclubs.edu/film_club",
  "description": "A welcoming community for collaboration and creativity.",
  "majors": "Finance, Economics"
}
```

### CRUD Operations
```python
# Create
collection.insert_one(club_data)

# Read
clubs = list(collection.find({}, {'_id': 0}))

# Update
collection.update_one({"club_name": name}, {"$set": data})

# Delete
collection.delete_one({"club_name": name})
```

---

## 5. AI Integration with Google Gemini

### Why Google Gemini?
- **Free tier** available
- **High-quality responses**
- **Easy integration**
- **Good for educational projects**

### Setting Up Gemini
```python
import google.generativeai as genai

# Configure API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Initialize model
model = genai.GenerativeModel('gemini-2.0-flash')
```

### Creating AI Prompts
```python
system_prompt = f"""You are a helpful assistant for Georgia Tech students looking for clubs to join.

Here are some available clubs at Georgia Tech:

{clubs_context}

Please help students find clubs that match their interests, majors, or goals."""
```

### Making AI Calls
```python
# Create full prompt
full_prompt = f"{system_prompt}\n\nUser: {user_message}\n\nAssistant:"

# Call Gemini API
response = model.generate_content(full_prompt)
bot_response = response.text
```

---

## 6. Frontend Development

### HTML Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>GT Club Chatbot</title>
    <style>
        /* CSS styles here */
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">GT Club Chatbot</div>
        <div class="chat-box" id="chat-box"></div>
        <div class="chat-input-container">
            <input type="text" id="user-input" placeholder="Type your message...">
            <button id="send-button">Send</button>
        </div>
    </div>
    <script>
        // JavaScript here
    </script>
</body>
</html>
```

### JavaScript API Calls
```javascript
async function sendMessage() {
    const message = userInput.value.trim();
    
    // Show loading indicator
    showLoadingIndicator();
    
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
```

### CSS Styling
```css
.chat-container {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    width: 90%;
    max-width: 600px;
    height: 80vh;
    display: flex;
    flex-direction: column;
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
```

---

## 7. Hands-on Coding Session

### Step 1: Project Setup
```bash
# Create project directory
mkdir gt_chatbot_workshop
cd gt_chatbot_workshop

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install flask pymongo python-dotenv pandas google-generativeai
```

### Step 2: Create Basic Flask App
```python
# hello.py
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return jsonify({"message": "Hello from Flask!"})

if __name__ == '__main__':
    app.run(debug=True, port=8001)
```

### Step 3: Add Database Integration
```python
# Add to hello.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGODB_CLIENT'), tlsAllowInvalidCertificates=True)
db = client["files"]
collection = db["clubs"]

@app.route('/clubs', methods=['GET'])
def get_all_clubs():
    try:
        clubs = list(collection.find({}, {'_id': 0}))
        return jsonify({
            'success': True,
            'clubs': clubs
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

### Step 4: Add AI Integration
```python
# Add to hello.py
import google.generativeai as genai

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        # Get clubs for context
        clubs = list(collection.find({}, {'_id': 0}))
        clubs_context = "\n".join([
            f"Club: {club['club_name']} - {club['description']}"
            for club in clubs[:10]
        ])
        
        # Create prompt
        prompt = f"""You are a helpful assistant for Georgia Tech students.
        
Available clubs:
{clubs_context}

User: {user_message}
Assistant:"""
        
        # Call Gemini
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        
        return jsonify({
            'success': True,
            'response': response.text
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

### Step 5: Create Frontend
```html
<!-- templates/index.html -->
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
        }
        .chat-container {
            border: 1px solid #ccc;
            height: 400px;
            overflow-y: auto;
            padding: 10px;
            margin-bottom: 10px;
        }
        .message {
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
        }
        .user {
            background-color: #e3f2fd;
            text-align: right;
        }
        .bot {
            background-color: #f5f5f5;
        }
        input[type="text"] {
            width: 70%;
            padding: 10px;
        }
        button {
            width: 25%;
            padding: 10px;
            margin-left: 5px;
        }
    </style>
</head>
<body>
    <h1>GT Club Chatbot</h1>
    <div class="chat-container" id="chatBox">
        <div class="message bot">Hello! I can help you find clubs at Georgia Tech. What are you interested in?</div>
    </div>
    <input type="text" id="userInput" placeholder="Type your message...">
    <button onclick="sendMessage()">Send</button>

    <script>
        function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            if (!message) return;
            
            // Add user message to chat
            addMessage(message, 'user');
            input.value = '';
            
            // Send to backend
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({message: message})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    addMessage(data.response, 'bot');
                } else {
                    addMessage('Error: ' + data.error, 'bot');
                }
            })
            .catch(error => {
                addMessage('Error: ' + error, 'bot');
            });
        }
        
        function addMessage(text, sender) {
            const chatBox = document.getElementById('chatBox');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            messageDiv.textContent = text;
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
        // Allow Enter key to send message
        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
```

---

## 8. Deployment and Best Practices

### Environment Variables
- **Never commit API keys** to version control
- Use `.env` files for local development
- Use environment variables in production

### Error Handling
```python
try:
    # API call or database operation
    result = some_operation()
    return jsonify({'success': True, 'data': result})
except Exception as e:
    return jsonify({'success': False, 'error': str(e)}), 500
```

### Security Best Practices
- Validate input data
- Use HTTPS in production
- Implement rate limiting
- Sanitize user inputs

### Testing Your API
```bash
# Test GET endpoint
curl http://localhost:8001/clubs

# Test POST endpoint
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What clubs are available?"}'
```

---

## 🎯 Workshop Demo Script

### Opening (5 minutes)
1. **Introduce yourself** and the project
2. **Show the final result** - working chatbot
3. **Explain the learning objectives**

### Part 1: API Concepts (15 minutes)
1. **What are APIs?** - Real-world examples
2. **HTTP methods** - GET, POST, PUT, DELETE
3. **JSON data format** - Show examples
4. **REST principles** - Stateless, uniform interface

### Part 2: Backend Development (30 minutes)
1. **Flask setup** - Live coding
2. **Environment variables** - Security best practices
3. **API endpoints** - Create basic endpoints
4. **Error handling** - Try/catch blocks

### Part 3: Database Integration (20 minutes)
1. **MongoDB setup** - Local installation
2. **Data modeling** - Document structure
3. **CRUD operations** - Live coding examples
4. **Data validation** - Input checking

### Part 4: AI Integration (25 minutes)
1. **Google Gemini setup** - API key configuration
2. **Prompt engineering** - Crafting effective prompts
3. **Context management** - Using database data
4. **Response handling** - Processing AI outputs

### Part 5: Frontend Development (30 minutes)
1. **HTML structure** - Semantic markup
2. **CSS styling** - Modern design principles
3. **JavaScript** - DOM manipulation and API calls
4. **User experience** - Loading states, error handling

### Part 6: Live Coding Session (45 minutes)
1. **Build together** - Step-by-step implementation
2. **Debug together** - Common issues and solutions
3. **Test together** - API testing and validation
4. **Enhance together** - Add new features

### Closing (10 minutes)
1. **Recap key concepts** - What we learned
2. **Next steps** - Further learning resources
3. **Q&A session** - Answer questions
4. **Project ideas** - Encourage experimentation

---

## 📚 Additional Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [MDN Web Docs](https://developer.mozilla.org/)

### Tools
- [Postman](https://www.postman.com/) - API testing
- [MongoDB Compass](https://www.mongodb.com/products/compass) - Database GUI
- [VS Code](https://code.visualstudio.com/) - Code editor

### Learning Paths
1. **Beginner**: HTML/CSS → JavaScript → Python → Flask
2. **Intermediate**: APIs → Databases → AI Integration
3. **Advanced**: Microservices → Cloud Deployment → DevOps

---

## 🎉 Workshop Success Metrics

### By the end of this workshop, participants should be able to:
- ✅ Understand what APIs are and how they work
- ✅ Build a basic Flask web application
- ✅ Connect to a MongoDB database
- ✅ Integrate with a third-party AI API
- ✅ Create a functional frontend interface
- ✅ Handle errors and edge cases
- ✅ Test their API endpoints
- ✅ Deploy their application

### Project Deliverables:
1. **Working chatbot application**
2. **Clean, documented code**
3. **API documentation**
4. **Deployment guide**
5. **Presentation slides**

---

*Happy coding! 🚀*
