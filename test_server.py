#!/usr/bin/env python3
"""
Basic tests for the MCP Android Server
"""

import requests
import json
import time
import subprocess
import threading
import sys
from contextlib import contextmanager

@contextmanager
def test_server():
    """Context manager to start and stop test server."""
    print("🚀 Starting test server...")
    process = subprocess.Popen([
        sys.executable, "mcp_server.py", "--port", "8002"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        yield "http://127.0.0.1:8002"
    finally:
        print("🛑 Stopping test server...")
        process.terminate()
        process.wait()

def test_endpoints():
    """Test all server endpoints."""
    print("🧪 Testing MCP Android Server Endpoints")
    print("=" * 50)
    
    with test_server() as base_url:
        # Test root endpoint
        try:
            response = requests.get(f"{base_url}/")
            assert response.status_code == 200
            data = response.json()
            assert data["success"] == True
            assert "MCP Android Server is running" in data["message"]
            print("✅ Root endpoint test passed")
        except Exception as e:
            print(f"❌ Root endpoint test failed: {e}")
            return False
        
        # Test health endpoint
        try:
            response = requests.get(f"{base_url}/health")
            assert response.status_code == 200
            data = response.json()
            # ADB won't be available in test environment, so success might be False
            assert "data" in data
            print("✅ Health endpoint test passed")
        except Exception as e:
            print(f"❌ Health endpoint test failed: {e}")
            return False
        
        # Test devices endpoint
        try:
            response = requests.get(f"{base_url}/devices")
            assert response.status_code == 200
            data = response.json()
            assert data["success"] == True
            assert "devices" in data["data"]
            print("✅ Devices endpoint test passed")
        except Exception as e:
            print(f"❌ Devices endpoint test failed: {e}")
            return False
        
        # Test tap endpoint (will fail due to no devices, but should validate request)
        try:
            response = requests.post(f"{base_url}/tap", json={
                "x": 100,
                "y": 200
            })
            # Expect 404 due to no devices connected
            assert response.status_code == 404
            data = response.json()
            assert "No Android devices connected" in data["detail"]
            print("✅ Tap endpoint validation test passed")
        except Exception as e:
            print(f"❌ Tap endpoint test failed: {e}")
            return False
        
        # Test swipe endpoint
        try:
            response = requests.post(f"{base_url}/swipe", json={
                "start_x": 100,
                "start_y": 200,
                "end_x": 300,
                "end_y": 400,
                "duration": 500
            })
            # Expect 404 due to no devices connected
            assert response.status_code == 404
            print("✅ Swipe endpoint validation test passed")
        except Exception as e:
            print(f"❌ Swipe endpoint test failed: {e}")
            return False
        
        # Test type endpoint
        try:
            response = requests.post(f"{base_url}/type", json={
                "text": "Hello World"
            })
            # Expect 404 due to no devices connected
            assert response.status_code == 404
            print("✅ Type endpoint validation test passed")
        except Exception as e:
            print(f"❌ Type endpoint test failed: {e}")
            return False
        
        # Test invalid requests
        try:
            response = requests.post(f"{base_url}/tap", json={
                "x": "invalid"  # Should be int
            })
            assert response.status_code == 422  # Validation error
            print("✅ Input validation test passed")
        except Exception as e:
            print(f"❌ Input validation test failed: {e}")
            return False
    
    print("\n🎉 All tests passed!")
    return True

if __name__ == "__main__":
    success = test_endpoints()
    sys.exit(0 if success else 1)