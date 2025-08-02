#!/usr/bin/env python3
"""
Lost Person Finder - Backend Server
Handles facial recognition, database operations, and API endpoints
"""

import os
import json
import sqlite3
import hashlib
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from deepface import DeepFace
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
DATABASE_FOLDER = 'database'
EXPORTS_FOLDER = 'exports'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

class FaceRecognitionSystem:
    def __init__(self):
        self.db_path = os.path.join(DATABASE_FOLDER, 'face_vectors.db')
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for face vectors"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS face_vectors (
                id TEXT PRIMARY KEY,
                person_type TEXT NOT NULL,
                person_id TEXT NOT NULL,
                photo_path TEXT NOT NULL,
                face_vector BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def extract_face_vector(self, image_path):
        """Extract face embedding vector from image"""
        try:
            # Use DeepFace to extract face embedding
            embedding = DeepFace.represent(
                img_path=image_path,
                model_name='VGG-Face',
                enforce_detection=False
            )
            return np.array(embedding[0]['embedding'])
        except Exception as e:
            logger.error(f"Error extracting face vector: {e}")
            return None
    
    def store_face_vector(self, person_type, person_id, photo_path):
        """Store face vector in database"""
        vector = self.extract_face_vector(photo_path)
        if vector is None:
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        vector_id = f"{person_type}_{person_id}_{hashlib.md5(photo_path.encode()).hexdigest()[:8]}"
        
        cursor.execute('''
            INSERT OR REPLACE INTO face_vectors 
            (id, person_type, person_id, photo_path, face_vector)
            VALUES (?, ?, ?, ?, ?)
        ''', (vector_id, person_type, person_id, photo_path, vector.tobytes()))
        
        conn.commit()
        conn.close()
        return True
    
    def find_matches(self, image_path, threshold=0.6):
        """Find matching faces in database"""
        query_vector = self.extract_face_vector(image_path)
        if query_vector is None:
            return []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM face_vectors')
        stored_vectors = cursor.fetchall()
        
        matches = []
        for row in stored_vectors:
            stored_vector = np.frombuffer(row[4], dtype=np.float64)
            
            # Calculate cosine similarity
            similarity = np.dot(query_vector, stored_vector) / (
                np.linalg.norm(query_vector) * np.linalg.norm(stored_vector)
            )
            
            if similarity > threshold:
                matches.append({
                    'person_type': row[1],
                    'person_id': row[2],
                    'photo_path': row[3],
                    'confidence': float(similarity),
                    'created_at': row[5]
                })
        
        conn.close()
        return sorted(matches, key=lambda x: x['confidence'], reverse=True)

# Initialize face recognition system
face_system = FaceRecognitionSystem()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_json_data(filename):
    """Load data from JSON file"""
    filepath = os.path.join(DATABASE_FOLDER, filename)
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_json_data(filename, data):
    """Save data to JSON file"""
    filepath = os.path.join(DATABASE_FOLDER, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    reports = load_json_data('reports.json')
    matches = load_json_data('matches.json')
    
    today = datetime.now().date()
    today_reports = 0
    
    # Count today's reports
    for person in reports.get('missing_persons', []):
        created_date = datetime.fromisoformat(person['created_at'].replace('Z', '+00:00')).date()
        if created_date == today:
            today_reports += 1
    
    for person in reports.get('found_persons', []):
        created_date = datetime.fromisoformat(person['created_at'].replace('Z', '+00:00')).date()
        if created_date == today:
            today_reports += 1
    
    return jsonify({
        'total_missing': len(reports.get('missing_persons', [])),
        'total_found': len(reports.get('found_persons', [])),
        'total_matches': len(matches.get('verified_matches', [])),
        'today_reports': today_reports
    })

@app.route('/api/reports/missing', methods=['POST'])
def submit_missing_report():
    """Submit a missing person report"""
    try:
        data = request.get_json()
        
        # Generate unique ID
        report_id = f"mp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create report object
        report = {
            'id': report_id,
            'reporter_name': data['reporterName'],
            'reporter_contact': data['reporterContact'],
            'relationship': data['relationship'],
            'missing_name': data['missingName'],
            'age': int(data['age']),
            'gender': data['gender'],
            'last_seen_date': data['lastSeenDate'],
            'last_seen_location': data['lastSeenLocation'],
            'height': int(data.get('height', 0)) if data.get('height') else None,
            'clothing': data.get('clothing', ''),
            'additional_details': data.get('additionalDetails', ''),
            'photos': [],
            'status': 'active',
            'created_at': datetime.now().isoformat() + 'Z',
            'updated_at': datetime.now().isoformat() + 'Z'
        }
        
        # Load existing reports
        reports = load_json_data('reports.json')
        if 'missing_persons' not in reports:
            reports['missing_persons'] = []
        
        reports['missing_persons'].append(report)
        save_json_data('reports.json', reports)
        
        return jsonify({'success': True, 'report_id': report_id})
        
    except Exception as e:
        logger.error(f"Error submitting missing report: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reports/found', methods=['POST'])
def submit_found_report():
    """Submit a found person report"""
    try:
        data = request.get_json()
        
        # Generate unique ID
        report_id = f"fp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create report object
        report = {
            'id': report_id,
            'finder_name': data['finderName'],
            'finder_contact': data['finderContact'],
            'found_date': data['foundDate'],
            'found_location': data['foundLocation'],
            'current_location': data.get('currentLocation', ''),
            'condition': data['condition'],
            'estimated_age': int(data.get('estimatedAge', 0)) if data.get('estimatedAge') else None,
            'estimated_gender': data.get('estimatedGender', ''),
            'notes': data.get('notes', ''),
            'photos': [],
            'status': 'unidentified',
            'created_at': datetime.now().isoformat() + 'Z',
            'updated_at': datetime.now().isoformat() + 'Z'
        }
        
        # Load existing reports
        reports = load_json_data('reports.json')
        if 'found_persons' not in reports:
            reports['found_persons'] = []
        
        reports['found_persons'].append(report)
        save_json_data('reports.json', reports)
        
        return jsonify({'success': True, 'report_id': report_id})
        
    except Exception as e:
        logger.error(f"Error submitting found report: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/upload/<report_type>/<report_id>', methods=['POST'])
def upload_photos(report_type, report_id):
    """Upload photos for a report"""
    try:
        if 'photos' not in request.files:
            return jsonify({'success': False, 'error': 'No photos provided'}), 400
        
        files = request.files.getlist('photos')
        uploaded_paths = []
        
        # Create directory if it doesn't exist
        upload_dir = os.path.join(UPLOAD_FOLDER, report_type)
        os.makedirs(upload_dir, exist_ok=True)
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{report_id}_{len(uploaded_paths) + 1}_{file.filename}")
                filepath = os.path.join(upload_dir, filename)
                file.save(filepath)
                
                # Store face vector
                face_system.store_face_vector(report_type, report_id, filepath)
                
                uploaded_paths.append(filepath)
        
        # Update report with photo paths
        reports = load_json_data('reports.json')
        report_key = 'missing_persons' if report_type == 'missing' else 'found_persons'
        
        for report in reports.get(report_key, []):
            if report['id'] == report_id:
                report['photos'] = uploaded_paths
                report['updated_at'] = datetime.now().isoformat() + 'Z'
                break
        
        save_json_data('reports.json', reports)
        
        return jsonify({'success': True, 'uploaded_files': uploaded_paths})
        
    except Exception as e:
        logger.error(f"Error uploading photos: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search_database():
    """Search database using facial recognition"""
    try:
        if 'photo' not in request.files:
            return jsonify({'success': False, 'error': 'No photo provided'}), 400
        
        file = request.files['photo']
        if not file or not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
        # Save uploaded search photo
        filename = secure_filename(f"search_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
        search_dir = os.path.join(UPLOAD_FOLDER, 'search')
        os.makedirs(search_dir, exist_ok=True)
        filepath = os.path.join(search_dir, filename)
        file.save(filepath)
        
        # Find matches
        matches = face_system.find_matches(filepath)
        
        # Get additional filters from request
        filters = request.form.to_dict()
        
        # Load reports to get full details
        reports = load_json_data('reports.json')
        detailed_matches = []
        
        for match in matches:
            person_type = match['person_type']
            person_id = match['person_id']
            
            # Find the person in reports
            report_key = 'missing_persons' if person_type == 'missing' else 'found_persons'
            for person in reports.get(report_key, []):
                if person['id'] == person_id:
                    detailed_matches.append({
                        'person': person,
                        'confidence': match['confidence'],
                        'match_type': person_type
                    })
                    break
        
        return jsonify({
            'success': True,
            'matches': detailed_matches[:10]  # Limit to top 10 matches
        })
        
    except Exception as e:
        logger.error(f"Error searching database: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reports/<report_type>', methods=['GET'])
def get_reports(report_type):
    """Get reports by type"""
    reports = load_json_data('reports.json')
    
    if report_type == 'missing':
        return jsonify(reports.get('missing_persons', []))
    elif report_type == 'found':
        return jsonify(reports.get('found_persons', []))
    else:
        return jsonify({'error': 'Invalid report type'}), 400

@app.route('/api/matches', methods=['GET'])
def get_matches():
    """Get all matches"""
    matches = load_json_data('matches.json')
    return jsonify(matches)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(DATABASE_FOLDER, exist_ok=True)
    os.makedirs(EXPORTS_FOLDER, exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)