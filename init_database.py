#!/usr/bin/env python3
"""
Database Initialization Script for Lost Person Finder
Creates necessary directories, database tables, and sample data
"""

import os
import json
import sqlite3
from datetime import datetime

def create_directories():
    """Create necessary directory structure"""
    directories = [
        'uploads',
        'uploads/missing',
        'uploads/found',
        'uploads/profiles',
        'uploads/search',
        'database',
        'exports',
        'exports/daily_reports',
        'exports/analytics'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def init_sqlite_database():
    """Initialize SQLite database for face vectors"""
    db_path = os.path.join('database', 'face_vectors.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Face vectors table
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
    
    # Matches table for tracking verified matches
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS verified_matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            missing_person_id TEXT NOT NULL,
            found_person_id TEXT NOT NULL,
            confidence_score REAL NOT NULL,
            verified_by TEXT,
            verification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending',
            notes TEXT
        )
    ''')
    
    # Search history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            search_image_path TEXT NOT NULL,
            search_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            results_count INTEGER DEFAULT 0,
            search_metadata TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Initialized SQLite database with tables")

def init_json_files():
    """Initialize JSON data files"""
    
    # Initialize reports.json if it doesn't exist or is empty
    reports_path = os.path.join('database', 'reports.json')
    if not os.path.exists(reports_path):
        reports_data = {
            "missing_persons": [],
            "found_persons": []
        }
        with open(reports_path, 'w') as f:
            json.dump(reports_data, f, indent=2)
        print("✓ Created empty reports.json")
    else:
        print("✓ reports.json already exists")
    
    # Initialize matches.json
    matches_path = os.path.join('database', 'matches.json')
    if not os.path.exists(matches_path):
        matches_data = {
            "verified_matches": [],
            "pending_matches": [],
            "rejected_matches": []
        }
        with open(matches_path, 'w') as f:
            json.dump(matches_data, f, indent=2)
        print("✓ Created empty matches.json")
    else:
        print("✓ matches.json already exists")

def create_sample_data():
    """Create sample data for testing (optional)"""
    response = input("Do you want to create sample data for testing? (y/n): ").lower()
    
    if response == 'y':
        # Sample data is already in reports.json, so we'll just confirm it
        print("✓ Sample data available in reports.json")
        
        # Create sample matches data
        matches_path = os.path.join('database', 'matches.json')
        sample_matches = {
            "verified_matches": [
                {
                    "id": 1,
                    "missing_person_id": "mp_001",
                    "found_person_id": "fp_001",
                    "confidence_score": 0.85,
                    "verified_by": "System Admin",
                    "verification_date": "2025-01-29T15:30:00Z",
                    "status": "verified",
                    "notes": "High confidence match confirmed by facial recognition"
                }
            ],
            "pending_matches": [],
            "rejected_matches": []
        }
        
        with open(matches_path, 'w') as f:
            json.dump(sample_matches, f, indent=2)
        print("✓ Created sample matches data")

def main():
    """Main initialization function"""
    print("Initializing Lost Person Finder Database...")
    print("=" * 50)
    
    try:
        # Create directory structure
        create_directories()
        
        # Initialize SQLite database
        init_sqlite_database()
        
        # Initialize JSON files
        init_json_files()
        
        # Optionally create sample data
        create_sample_data()
        
        print("\n" + "=" * 50)
        print("✅ Database initialization completed successfully!")
        print("\nNext steps:")
        print("1. Install required dependencies: pip install flask flask-cors opencv-python deepface")
        print("2. Run the server: python server.py")
        print("3. Access the API at http://localhost:5000")
        
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()