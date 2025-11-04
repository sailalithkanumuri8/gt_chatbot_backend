#!/usr/bin/env python3
"""Quick test script to verify MongoDB connection"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure

load_dotenv()

mongodb_client = os.getenv('MONGODB_CLIENT')
print(f"Testing connection string: {mongodb_client[:50]}...")

try:
    print("\n1. Creating MongoDB client...")
    client = MongoClient(
        mongodb_client,
        tlsAllowInvalidCertificates=True,
        serverSelectionTimeoutMS=10000  # 10 second timeout
    )
    
    print("2. Testing connection...")
    client.admin.command('ping')
    print("✓ Connection successful!")
    
    print("3. Testing database access...")
    db = client["files"]
    collection = db["clubs"]
    
    count = collection.count_documents({})
    print(f"✓ Database accessible! Found {count} clubs in collection.")
    
    print("\n✅ All tests passed! Your MongoDB connection is working.")
    print("You can now run: python upload_clubs.py")
    
except ServerSelectionTimeoutError as e:
    print(f"\n✗ Connection timeout: {e}")
    print("\nPossible issues:")
    print("  - IP address not whitelisted in MongoDB Atlas")
    print("  - Internet connection problem")
    print("  - MongoDB cluster is down")
    
except OperationFailure as e:
    print(f"\n✗ Authentication failed: {e}")
    print("\nPossible issues:")
    print("  - Username or password is incorrect")
    print("  - Database user doesn't exist")
    print("  - Database user doesn't have proper permissions")
    
except Exception as e:
    print(f"\n✗ Unexpected error: {e}")
    import traceback
    traceback.print_exc()

finally:
    if 'client' in locals():
        client.close()
        print("\nConnection closed.")


