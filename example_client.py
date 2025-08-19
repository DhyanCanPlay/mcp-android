#!/usr/bin/env python3
"""
Example MCP Android Client
Demonstrates how to interact with the MCP Android Server
"""

import requests
import json
import time

class MCPAndroidClient:
    def __init__(self, server_url="http://localhost:5000"):
        self.server_url = server_url
        self.session = requests.Session()
    
    def check_health(self):
        """Check server health and device connection status"""
        try:
            response = self.session.get(f"{self.server_url}/health")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def send_command(self, command, params):
        """Send a command to the MCP server"""
        try:
            payload = {"command": command, "params": params}
            response = self.session.post(
                f"{self.server_url}/mcp/command", 
                json=payload,
                timeout=30
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def enable_wifi(self):
        """Enable WiFi on the device"""
        return self.send_command("setWifiState", {"state": True})
    
    def disable_wifi(self):
        """Disable WiFi on the device"""
        return self.send_command("setWifiState", {"state": False})
    
    def enable_bluetooth(self):
        """Enable Bluetooth on the device"""
        return self.send_command("setBluetoothState", {"state": True})
    
    def disable_bluetooth(self):
        """Disable Bluetooth on the device"""
        return self.send_command("setBluetoothState", {"state": False})
    
    def turn_on_torch(self, brightness=100):
        """Turn on the camera torch/flashlight"""
        params = {"state": True}
        if brightness != 100:
            params["brightnessLevel"] = brightness
        return self.send_command("setTorchState", params)
    
    def turn_off_torch(self):
        """Turn off the camera torch/flashlight"""
        return self.send_command("setTorchState", {"state": False})
    
    def tap_screen(self, x, y):
        """Tap the screen at specific coordinates"""
        return self.send_command("tap", {"x": x, "y": y})
    
    def long_press(self, x, y, duration_ms=1000):
        """Long press at specific coordinates"""
        return self.send_command("longPress", {
            "x": x, "y": y, "durationMs": duration_ms
        })
    
    def swipe(self, start_x, start_y, end_x, end_y, duration_ms=500):
        """Swipe from start coordinates to end coordinates"""
        return self.send_command("swipe", {
            "startX": start_x, "startY": start_y,
            "endX": end_x, "endY": end_y,
            "durationMs": duration_ms
        })
    
    def get_screen_brightness(self):
        """Get current screen brightness setting"""
        return self.send_command("getSystemSetting", {"key": "screen_brightness"})
    
    def set_screen_timeout(self, timeout_ms):
        """Set screen timeout in milliseconds"""
        return self.send_command("setSystemSetting", {
            "key": "screen_off_timeout", 
            "value": str(timeout_ms)
        })
    
    def get_sensor_data(self, sensor_type):
        """Get data from a specific sensor"""
        return self.send_command("getSensorData", {"sensorType": sensor_type})

def demo_usage():
    """Demonstrate basic usage of the MCP Android Client"""
    print("=== MCP Android Client Demo ===\n")
    
    client = MCPAndroidClient()
    
    # Check health
    print("1. Checking server health...")
    health = client.check_health()
    print(f"   Status: {health}")
    
    if not health.get("device_connected", False):
        print("\n⚠️  No Android device connected. Commands will fail but demonstrate API usage.\n")
    
    # Demonstrate hardware control
    print("2. Hardware Control Examples:")
    print("   - Enabling WiFi...")
    result = client.enable_wifi()
    print(f"     Result: {result}")
    
    print("   - Turning on torch...")
    result = client.turn_on_torch(brightness=50)
    print(f"     Result: {result}")
    
    # Demonstrate screen interaction
    print("\n3. Screen Interaction Examples:")
    print("   - Tapping center of screen...")
    result = client.tap_screen(540, 960)
    print(f"     Result: {result}")
    
    print("   - Swiping up...")
    result = client.swipe(540, 1500, 540, 500, 300)
    print(f"     Result: {result}")
    
    # Demonstrate system settings
    print("\n4. System Settings Examples:")
    print("   - Getting screen brightness...")
    result = client.get_screen_brightness()
    print(f"     Result: {result}")
    
    print("   - Getting accelerometer data...")
    result = client.get_sensor_data("accelerometer")
    print(f"     Result: {result}")
    
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo_usage()