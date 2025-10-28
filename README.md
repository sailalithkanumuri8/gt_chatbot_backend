# GT Chatbot Backend

A simple Flask backend with MongoDB integration for managing club data.

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/sailalithkanumuri8/gt_chatbot_backend.git
   cd gt_chatbot_backend
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask pymongo python-dotenv pandas
   ```

4. **Create `.env` file**
   ```bash
   echo "MONGODB_CLIENT=your_mongodb_connection_string_here" > .env
   ```

## Usage

1. **Upload data to MongoDB**
   ```bash
   python upload_clubs.py
   ```

2. **Start the Flask server**
   ```bash
   python hello.py
   ```

3. **Test the API**
   - Get all clubs: `http://localhost:8001/clubs`
   - Get specific club: `http://localhost:8001/clubs/Finance%20Association`

## API Endpoints

- `GET /clubs` - Returns all clubs
- `GET /clubs/<club_name>` - Returns clubs matching the name (case-insensitive)

## Files

- `hello.py` - Flask application with API endpoints
- `upload_clubs.py` - Script to upload CSV data to MongoDB
- `sample_clubs.csv` - Sample club data
- `.env` - MongoDB connection string (create this file)
