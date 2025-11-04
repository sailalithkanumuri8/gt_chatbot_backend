import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    # Get MongoDB connection string
    mongodb_client = os.getenv('MONGODB_CLIENT')
    if not mongodb_client or mongodb_client == 'your_mongodb_connection_string_here':
        raise ValueError("MONGODB_CLIENT not set in .env file")
    
    # Connect to MongoDB with timeout
    print("Connecting to MongoDB...")
    client = MongoClient(
        mongodb_client, 
        tlsAllowInvalidCertificates=True,
        serverSelectionTimeoutMS=5000  # 5 second timeout
    )
    # Test the connection
    client.admin.command('ping')
    db = client["files"]
    collection = db["clubs"]
    print("✓ Connected to MongoDB")
    
    # Read CSV file
    print("Reading sample_clubs.csv...")
    if not os.path.exists('sample_clubs.csv'):
        raise FileNotFoundError("sample_clubs.csv not found in current directory")
    
    df = pd.read_csv('sample_clubs.csv')
    clubs_data = df.to_dict('records')
    print(f"✓ Loaded {len(clubs_data)} clubs from CSV")
    
    # Check if collection already has data
    print("Checking for existing clubs...")
    existing_count = collection.count_documents({})
    if existing_count > 0:
        print(f"⚠ Warning: Collection already has {existing_count} clubs.")
        print("⚠ Clearing existing data and uploading fresh data...")
        collection.delete_many({})
        print("✓ Cleared existing clubs")
    
    # Upload to MongoDB
    print("Uploading clubs to MongoDB...")
    result = collection.insert_many(clubs_data)
    print(f"✓ Successfully uploaded {len(result.inserted_ids)} clubs to MongoDB")
    
    # Verify upload
    total_count = collection.count_documents({})
    print(f"✓ Total clubs in database: {total_count}")
    
except FileNotFoundError as e:
    print(f"✗ Error: {e}")
except ValueError as e:
    print(f"✗ Error: {e}")
except Exception as e:
    error_type = type(e).__name__
    if 'ServerSelectionTimeoutError' in error_type or 'timeout' in str(e).lower():
        print(f"✗ MongoDB connection timeout. Please check:")
        print(f"  - Your internet connection")
        print(f"  - MongoDB connection string in .env file")
        print(f"  - IP address whitelist in MongoDB Atlas")
    else:
        print(f"✗ Error uploading clubs: {e}")
    import traceback
    traceback.print_exc()
finally:
    if 'client' in locals():
        client.close()
        print("✓ MongoDB connection closed")