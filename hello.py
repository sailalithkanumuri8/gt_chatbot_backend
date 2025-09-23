from flask import Flask, jsonify
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/clubs', methods=['GET'])
def get_clubs():
    df = pd.read_csv('sample_clubs.csv')
    return jsonify(df.to_dict('records'))

@app.route('/clubs/<club_name>', methods=['GET'])
def get_club_by_name(club_name):
    df = pd.read_csv('sample_clubs.csv')
    club_data = df[df['club_name'].str.lower() == club_name.lower()]
    return jsonify(club_data.to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True)