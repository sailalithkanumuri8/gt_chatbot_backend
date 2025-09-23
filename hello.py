from flask import Flask, jsonify
from pymongo import MongoClient
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_CLIENT'))
db = client["files"]
collection = db["clubs"]

def get_clubs_dataframe():
    """Fetch data from MongoDB and return as pandas DataFrame"""
    clubs_data = list(collection.find({}, {'_id': 0}))
    return pd.DataFrame(clubs_data)

@app.route('/clubs', methods=['GET'])
def get_clubs():
    df = get_clubs_dataframe()
    return jsonify(df.to_dict('records'))

@app.route('/clubs/<club_name>', methods=['GET'])
def get_club_by_name(club_name):
    df = get_clubs_dataframe()
    club_data = df[df['club_name'].str.lower() == club_name.lower()]
    return jsonify(club_data.to_dict('records'))


# TODO
# Implement a POST endpoint to update a club
# Implement a POST endpoint to delete a club
# Implement a POST endpoint to create a club

if __name__ == '__main__':
    app.run(debug=True)