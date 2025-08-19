#!/usr/bin/env python3
"""
Test script for MCP Android Server
"""

import requests
import json
import sys

SERVER_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{SERVER_URL}/health")
        print(f"Health Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_command(command, params):
    """Test a specific MCP command"""
    print(f"\nTesting command: {command}")
    print(f"Parameters: {params}")
    
    try:
        payload = {
            "command": command,
            "params": params
        }
        
        response = requests.post(f"{SERVER_URL}/mcp/command", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Command test failed: {e}")
        return False

def main():
    """Run basic tests"""
    print("=== MCP Android Server Test Suite ===\n")
    
    # Test health
    if not test_health():
        print("Server is not healthy. Exiting.")
        sys.exit(1)
    
    # Test commands (these will fail if no device is connected, but structure will be validated)
    test_cases = [
        ("tap", {"x": 100, "y": 200}),
        ("setWifiState", {"state": True}),
        ("getSystemSetting", {"key": "screen_brightness"}),
        ("getSensorData", {"sensorType": "accelerometer"}),
        ("swipe", {"startX": 100, "startY": 100, "endX": 200, "endY": 200, "durationMs": 500})
    ]
    
    for command, params in test_cases:
        test_command(command, params)
    
    print("\n=== Test Suite Complete ===")

if __name__ == "__main__":
    main()