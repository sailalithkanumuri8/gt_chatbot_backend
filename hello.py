from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import pandas as pd
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

app = Flask(__name__)

# LIVE CODE TASK 1: Database Connection (5 minutes)
# TODO: Add database connection code here


# LIVE CODE TASK 2: AI API Setup (3 minutes)
# TODO: Add AI API configuration here

@app.route('/clubs', methods=['GET'])
def get_all_clubs():
    """Get all clubs from the database"""
    try:
        clubs = list(collection.find({}, {'_id': 0}))
        return jsonify({
            'success': True,
            'count': len(clubs),
            'clubs': clubs
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/clubs/<club_name>', methods=['GET'])
def get_club_by_name(club_name):
    """Get clubs matching the name (case-insensitive)"""
    try:
        # Case-insensitive search using regex
        clubs = list(collection.find(
            {'club_name': {'$regex': club_name, '$options': 'i'}}, 
            {'_id': 0}
        ))
        return jsonify({
            'success': True,
            'count': len(clubs),
            'clubs': clubs
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/clubs', methods=['POST'])
def create_club():
    """Create a new club"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['club_name', 'link', 'description', 'majors']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Insert the new club
        result = collection.insert_one(data)
        
        return jsonify({
            'success': True,
            'message': 'Club created successfully',
            'club_id': str(result.inserted_id)
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/clubs/<club_name>', methods=['PUT'])
def update_club(club_name):
    """Update a club by name"""
    try:
        data = request.get_json()
        
        # Remove _id if present to avoid conflicts
        if '_id' in data:
            del data['_id']
        
        # Update the club (case-insensitive search)
        result = collection.update_many(
            {'club_name': {'$regex': club_name, '$options': 'i'}},
            {'$set': data}
        )
        
        if result.modified_count > 0:
            return jsonify({
                'success': True,
                'message': f'Updated {result.modified_count} club(s)',
                'modified_count': result.modified_count
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No clubs found with that name'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/clubs/<club_name>', methods=['DELETE'])
def delete_club(club_name):
    """Delete clubs by name (case-insensitive)"""
    try:
        # Delete clubs matching the name (case-insensitive)
        result = collection.delete_many(
            {'club_name': {'$regex': club_name, '$options': 'i'}}
        )
        
        if result.deleted_count > 0:
            return jsonify({
                'success': True,
                'message': f'Deleted {result.deleted_count} club(s)',
                'deleted_count': result.deleted_count
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No clubs found with that name'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/')
def index():
    """Serve the main chatbot UI"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages with Gemini"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400

        # LIVE CODE TASK 3: Data Retrieval for AI Context (5 minutes)
        # TODO: Get clubs from database and format for AI


        # LIVE CODE TASK 4: AI Prompt Engineering (7 minutes)
        # TODO: Create system prompt with club information
        

        # LIVE CODE TASK 5: AI API Call (5 minutes)
        # TODO: Call Gemini API and get response

        return jsonify({
            'success': True,
            'response': bot_response
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=8002)