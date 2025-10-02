# 🚀 API Integration Workshop: Building a GT Club Chatbot
## Presentation Slides

---

## Slide 1: Welcome & Introduction
### Building a GT Club Chatbot with APIs
**Presenter:** [Your Name]  
**Duration:** 2-3 hours  
**Level:** Beginner to Intermediate

**What we'll build today:**
- 🤖 AI-powered chatbot for GT students
- 🔗 REST API with Flask
- 🗄️ MongoDB database integration
- 🎨 Modern web frontend
- ☁️ Google Gemini AI integration

---

## Slide 2: What is an API?
### Application Programming Interface

**Think of an API like a waiter in a restaurant:**
- You (client) give your order to the waiter
- Waiter (API) takes it to the kitchen (server)
- Kitchen prepares your food (processes request)
- Waiter brings back your food (returns response)

**Real-world examples:**
- Weather apps use weather APIs
- Social media apps use platform APIs
- Payment apps use banking APIs

---

## Slide 3: Types of APIs
### Different Ways to Communicate

**REST APIs** (what we're building)
- Uses HTTP methods (GET, POST, PUT, DELETE)
- Stateless communication
- JSON data format

**Other types:**
- GraphQL APIs
- WebSocket APIs
- SOAP APIs

**Our focus:** REST APIs with JSON

---

## Slide 4: HTTP Methods Explained
### The Language of APIs

```
GET    📥 Retrieve data
POST   📤 Create new data
PUT    🔄 Update existing data
DELETE 🗑️ Remove data
```

**Examples:**
- `GET /clubs` - Get all clubs
- `POST /clubs` - Create new club
- `PUT /clubs/123` - Update club 123
- `DELETE /clubs/123` - Delete club 123

---

## Slide 5: Our Project Architecture
### The Big Picture

```
┌─────────────────┐    HTTP Requests    ┌─────────────────┐
│   Frontend      │◄──────────────────►│   Backend       │
│   (HTML/CSS/JS) │                    │   (Flask)       │
└─────────────────┘                    └─────────────────┘
                                                │
                                                │ Database Queries
                                                ▼
                                       ┌─────────────────┐
                                       │   Database      │
                                       │   (MongoDB)     │
                                       └─────────────────┘
                                                │
                                                │ API Calls
                                                ▼
                                       ┌─────────────────┐
                                       │   AI Service    │
                                       │   (Gemini)      │
                                       └─────────────────┘
```

---

## Slide 6: Flask Backend Setup
### Python Web Framework

**Why Flask?**
- Lightweight and flexible
- Great for learning
- Easy to understand
- Perfect for APIs

**Basic Flask app:**
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({"message": "Hello World!"})

if __name__ == '__main__':
    app.run(debug=True, port=8001)
```

---

## Slide 7: Environment Variables
### Keeping Secrets Safe

**Never commit API keys to code!**

**.env file:**
```bash
MONGODB_CLIENT=mongodb://localhost:27017/
GEMINI_API_KEY=your_secret_key_here
```

**Loading in Python:**
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
```

**Security best practice:** Use `.gitignore` to exclude `.env` files

---

## Slide 8: MongoDB Database
### NoSQL Database for Flexibility

**Why MongoDB?**
- Document-based (like JSON)
- Flexible schema
- Easy to scale
- Perfect for club data

**Sample document:**
```json
{
  "club_name": "Film Club",
  "description": "A welcoming community for creativity",
  "majors": "Finance, Economics",
  "link": "https://example.com/film-club"
}
```

---

## Slide 9: Database Operations
### CRUD with MongoDB

**Create (Insert):**
```python
collection.insert_one({
    "club_name": "New Club",
    "description": "A great club!"
})
```

**Read (Find):**
```python
clubs = list(collection.find({}, {'_id': 0}))
```

**Update:**
```python
collection.update_one(
    {"club_name": "Film Club"},
    {"$set": {"description": "Updated description"}}
)
```

**Delete:**
```python
collection.delete_one({"club_name": "Old Club"})
```

---

## Slide 10: Google Gemini AI
### Adding Intelligence to Our App

**Why Gemini?**
- Free tier available
- High-quality responses
- Easy integration
- Great for educational projects

**Setup:**
```python
import google.generativeai as genai

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')
```

---

## Slide 11: AI Prompt Engineering
### Teaching AI to Help Students

**Good prompts include:**
- Clear role definition
- Context about the data
- Specific instructions
- Examples of desired output

**Our prompt:**
```python
prompt = f"""You are a helpful assistant for Georgia Tech students.

Available clubs:
{clubs_context}

User: {user_message}
Assistant:"""
```

---

## Slide 12: Frontend Development
### Making It User-Friendly

**HTML Structure:**
- Semantic markup
- Accessible design
- Mobile-responsive

**CSS Styling:**
- Modern design principles
- Consistent color scheme
- Smooth animations

**JavaScript:**
- DOM manipulation
- API calls with fetch()
- Error handling

---

## Slide 13: API Communication
### Frontend to Backend

**Sending data to backend:**
```javascript
const response = await fetch('/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({message: userMessage})
});
```

**Handling responses:**
```javascript
const data = await response.json();
if (data.success) {
    displayMessage(data.response);
} else {
    showError(data.error);
}
```

---

## Slide 14: Error Handling
### Graceful Failure

**Always handle errors:**
```python
try:
    result = risky_operation()
    return jsonify({'success': True, 'data': result})
except Exception as e:
    return jsonify({'success': False, 'error': str(e)}), 500
```

**Frontend error handling:**
```javascript
try {
    const response = await fetch('/api/endpoint');
    const data = await response.json();
    // Handle success
} catch (error) {
    // Handle error
    console.error('Error:', error);
}
```

---

## Slide 15: Testing Your API
### Making Sure It Works

**Command line testing:**
```bash
# Test GET endpoint
curl http://localhost:8001/clubs

# Test POST endpoint
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What clubs are available?"}'
```

**Browser testing:**
- Visit `http://localhost:8001`
- Use browser developer tools
- Check network tab for API calls

---

## Slide 16: Live Coding Demo
### Let's Build It Together!

**Step 1:** Project setup
**Step 2:** Basic Flask app
**Step 3:** Database integration
**Step 4:** AI integration
**Step 5:** Frontend development
**Step 6:** Testing and debugging

**Follow along:**
- Create your own project
- Ask questions anytime
- Experiment with the code

---

## Slide 17: Common Issues & Solutions
### Debugging Tips

**Database connection issues:**
- Check MongoDB is running
- Verify connection string
- Check firewall settings

**API key problems:**
- Verify key is correct
- Check environment variables
- Ensure key has proper permissions

**CORS errors:**
- Add CORS headers
- Check request origins
- Use proper HTTP methods

---

## Slide 18: Best Practices
### Writing Production-Ready Code

**Security:**
- Never expose API keys
- Validate all inputs
- Use HTTPS in production
- Implement rate limiting

**Code Quality:**
- Write clear comments
- Use meaningful variable names
- Follow PEP 8 (Python style guide)
- Write tests

**Performance:**
- Use database indexes
- Implement caching
- Optimize API responses
- Monitor performance

---

## Slide 19: Next Steps
### Continue Your Learning Journey

**Immediate next steps:**
- Deploy your app to the cloud
- Add user authentication
- Implement real-time features
- Add more AI capabilities

**Learning resources:**
- Flask documentation
- MongoDB tutorials
- JavaScript MDN docs
- Google Gemini API docs

**Project ideas:**
- Personal portfolio site
- E-commerce API
- Social media app
- IoT dashboard

---

## Slide 20: Q&A Session
### Questions & Answers

**Common questions:**
- How do I deploy this to production?
- Can I use a different database?
- How do I add user accounts?
- What other AI models can I use?

**Ask anything:**
- Technical questions
- Project ideas
- Career advice
- Learning resources

**Contact info:**
- [Your email]
- [GitHub profile]
- [LinkedIn profile]

---

## Slide 21: Workshop Summary
### What We Accomplished

**✅ Built a complete web application**
- Flask backend with REST API
- MongoDB database integration
- Google Gemini AI integration
- Modern responsive frontend

**✅ Learned key concepts**
- API design and development
- Database operations
- AI integration
- Frontend development

**✅ Gained practical skills**
- Error handling
- Testing techniques
- Security best practices
- Code organization

---

## Slide 22: Thank You!
### Keep Building Amazing Things

**Remember:**
- Start small, think big
- Practice regularly
- Join developer communities
- Never stop learning

**Your next project awaits!**
- Build something you're passionate about
- Share your work with others
- Contribute to open source
- Help others learn

**Happy coding! 🚀**

---

## Appendix: Code Examples
### Quick Reference

### Complete Flask App Structure
```python
from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Database setup
client = MongoClient(os.getenv('MONGODB_CLIENT'))
db = client["files"]
collection = db["clubs"]

# AI setup
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clubs', methods=['GET'])
def get_clubs():
    clubs = list(collection.find({}, {'_id': 0}))
    return jsonify({'success': True, 'clubs': clubs})

@app.route('/chat', methods=['POST'])
def chat():
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
    
    # Get AI response
    response = model.generate_content(prompt)
    
    return jsonify({
        'success': True,
        'response': response.text
    })

if __name__ == '__main__':
    app.run(debug=True, port=8001)
```

### Complete Frontend HTML
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GT Club Chatbot</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
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
            color: white;
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
            color: white;
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

            const loadingDiv = document.createElement('div');
            loadingDiv.classList.add('message', 'bot');
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
