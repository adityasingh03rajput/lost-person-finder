#!/usr/bin/env python3
"""
Simple API test script for Lost Person Finder
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Health Check: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_stats():
    """Test stats endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/stats")
        print(f"Stats: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"Stats test failed: {e}")
        return False

def test_missing_reports():
    """Test getting missing reports"""
    try:
        response = requests.get(f"{BASE_URL}/api/reports/missing")
        print(f"Missing Reports: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"Missing reports test failed: {e}")
        return False

def test_found_reports():
    """Test getting found reports"""
    try:
        response = requests.get(f"{BASE_URL}/api/reports/found")
        print(f"Found Reports: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"Found reports test failed: {e}")
        return False

def main():
    print("Testing Lost Person Finder API...")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Statistics", test_stats),
        ("Missing Reports", test_missing_reports),
        ("Found Reports", test_found_reports)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 20)
        success = test_func()
        results.append((test_name, success))
    
    print("\n" + "=" * 50)
    print("Test Results:")
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")

if __name__ == "__main__":
    main()