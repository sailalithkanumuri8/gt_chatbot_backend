from flask import Flask, jsonify
from pymongo import MongoClient
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv('MONGODB_CLIENT'), tlsAllowInvalidCertificates=True)


# TODO
# Implement a POST endpoint to update a club
# Implement a POST endpoint to delete a club
# Implement a POST endpoint to create a club

if __name__ == '__main__':
    app.run(debug=True, port=8000)