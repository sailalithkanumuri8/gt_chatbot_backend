import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = MongoClient(os.getenv('MONGODB_CLIENT'), tlsAllowInvalidCertificates=True)
db = client["files"]
collection = db["clubs"]

# Read CSV and upload to MongoDB
df = pd.read_csv('sample_clubs.csv')
clubs_data = df.to_dict('records')

collection.insert_many(clubs_data)
print(f"Uploaded {len(clubs_data)} clubs to MongoDB")

client.close()

