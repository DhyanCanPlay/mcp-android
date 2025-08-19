#!/usr/bin/env python3
"""
Example usage of the MCP Android Server
"""

import requests
import json
import time

# Server configuration
SERVER_URL = "http://127.0.0.1:8000"

def test_server():
    """Test basic server functionality."""
    print("🤖 Testing MCP Android Server")
    print("=" * 40)
    
    # Test server health
    try:
        response = requests.get(f"{SERVER_URL}/health")
        health_data = response.json()
        print(f"✅ Server Health: {health_data['message']}")
        print(f"   ADB Available: {health_data['data']['adb_available']}")
        print(f"   Connected Devices: {health_data['data']['connected_devices']}")
        
        if health_data['data']['connected_devices'] == 0:
            print("⚠️  No Android devices connected. Please connect a device to test commands.")
            return
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the server is running.")
        return
    
    # Get device list
    response = requests.get(f"{SERVER_URL}/devices")
    devices_data = response.json()
    print(f"📱 Available devices: {devices_data['data']['devices']}")
    
    if not devices_data['data']['devices']:
        print("⚠️  No devices available for testing.")
        return
    
    # Test commands
    print("\n🎯 Testing Commands")
    print("-" * 20)
    
    # Test tap
    print("Testing tap command...")
    tap_response = requests.post(f"{SERVER_URL}/tap", json={
        "x": 500,
        "y": 500
    })
    print(f"Tap result: {tap_response.json()['message']}")
    time.sleep(1)
    
    # Test swipe
    print("Testing swipe command...")
    swipe_response = requests.post(f"{SERVER_URL}/swipe", json={
        "start_x": 300,
        "start_y": 800,
        "end_x": 700,
        "end_y": 800,
        "duration": 500
    })
    print(f"Swipe result: {swipe_response.json()['message']}")
    time.sleep(1)
    
    # Test type (note: this requires an active text input field)
    print("Testing type command...")
    type_response = requests.post(f"{SERVER_URL}/type", json={
        "text": "Hello from MCP!"
    })
    print(f"Type result: {type_response.json()['message']}")
    
    print("\n✅ Testing complete!")

if __name__ == "__main__":
    test_server()