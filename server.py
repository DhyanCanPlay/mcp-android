import os
import json
import subprocess
from flask import Flask, request, jsonify
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class MCPAndroidServer:
    """MCP Android Control Server"""
    
    def __init__(self):
        self.device_id = None
        self._check_adb_connection()
    
    def _check_adb_connection(self):
        """Check if ADB is available and device is connected"""
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            if result.returncode == 0:
                devices = [line for line in result.stdout.split('\n')[1:] if line.strip() and 'device' in line]
                if devices:
                    self.device_id = devices[0].split('\t')[0]
                    logger.info(f"Connected to Android device: {self.device_id}")
                else:
                    logger.warning("No Android devices connected")
            else:
                logger.error("ADB not available")
        except FileNotFoundError:
            logger.error("ADB not found. Please install Android Debug Bridge (ADB)")
    
    def _execute_adb_command(self, command: list) -> Dict[str, Any]:
        """Execute ADB command and return result"""
        if not self.device_id:
            return {"success": False, "error": "No Android device connected"}
        
        try:
            full_command = ['adb', '-s', self.device_id] + command
            result = subprocess.run(full_command, capture_output=True, text=True, timeout=30)
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}

# Initialize the server
mcp_server = MCPAndroidServer()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "device_connected": mcp_server.device_id is not None,
        "device_id": mcp_server.device_id
    })

@app.route('/mcp/command', methods=['POST'])
def handle_mcp_command():
    """Main MCP command handler"""
    try:
        data = request.get_json()
        if not data or 'command' not in data:
            return jsonify({"success": False, "error": "Invalid request format"}), 400
        
        command = data['command']
        params = data.get('params', {})
        
        # Route command to appropriate handler
        if command in ['setWifiState', 'setBluetoothState', 'setTorchState', 'getSensorData']:
            return jsonify(handle_hardware_control(command, params))
        elif command in ['tap', 'longPress', 'swipe']:
            return jsonify(handle_screen_interaction(command, params))
        elif command in ['getSystemSetting', 'setSystemSetting']:
            return jsonify(handle_system_settings(command, params))
        else:
            return jsonify({"success": False, "error": f"Unknown command: {command}"}), 400
            
    except Exception as e:
        logger.error(f"Error handling command: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

def handle_hardware_control(command: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle hardware control commands"""
    
    if command == 'setWifiState':
        state = params.get('state')
        if state is None:
            return {"success": False, "error": "Parameter 'state' is required"}
        
        wifi_command = 'enable' if state else 'disable'
        result = mcp_server._execute_adb_command(['shell', 'svc', 'wifi', wifi_command])
        
        if result['success']:
            return {"success": True, "message": f"WiFi {'enabled' if state else 'disabled'}"}
        else:
            return {"success": False, "error": f"Failed to set WiFi state: {result.get('stderr', 'Unknown error')}"}
    
    elif command == 'setBluetoothState':
        state = params.get('state')
        if state is None:
            return {"success": False, "error": "Parameter 'state' is required"}
        
        bt_command = 'enable' if state else 'disable'
        result = mcp_server._execute_adb_command(['shell', 'svc', 'bluetooth', bt_command])
        
        if result['success']:
            return {"success": True, "message": f"Bluetooth {'enabled' if state else 'disabled'}"}
        else:
            return {"success": False, "error": f"Failed to set Bluetooth state: {result.get('stderr', 'Unknown error')}"}
    
    elif command == 'setTorchState':
        state = params.get('state')
        if state is None:
            return {"success": False, "error": "Parameter 'state' is required"}
        
        # For torch control, we'll use a simple approach with camera2 API via shell commands
        if state:
            # Turn on torch
            result = mcp_server._execute_adb_command([
                'shell', 'echo', '1', '>', '/sys/class/leds/flashlight/brightness'
            ])
        else:
            # Turn off torch
            result = mcp_server._execute_adb_command([
                'shell', 'echo', '0', '>', '/sys/class/leds/flashlight/brightness'
            ])
        
        if result['success']:
            return {"success": True, "message": f"Torch {'enabled' if state else 'disabled'}"}
        else:
            # Fallback: try alternative torch control method
            torch_value = '1' if state else '0'
            result = mcp_server._execute_adb_command([
                'shell', 'su', '-c', f'echo {torch_value} > /sys/class/leds/flashlight/brightness'
            ])
            
            if result['success']:
                return {"success": True, "message": f"Torch {'enabled' if state else 'disabled'}"}
            else:
                return {"success": False, "error": "Failed to control torch. Device may not support this feature or requires root access."}
    
    elif command == 'getSensorData':
        sensor_type = params.get('sensorType')
        if not sensor_type:
            return {"success": False, "error": "Parameter 'sensorType' is required"}
        
        # Get sensor data using Android's dumpsys
        result = mcp_server._execute_adb_command(['shell', 'dumpsys', 'sensorservice'])
        
        if result['success']:
            # Parse sensor data (simplified implementation)
            sensor_data = {
                "sensorType": sensor_type,
                "timestamp": "current",
                "data": "Sensor data parsing would be implemented here based on sensor type",
                "raw_output": result['stdout'][:500]  # Truncated for demo
            }
            return {"success": True, "sensorData": sensor_data}
        else:
            return {"success": False, "error": f"Failed to get sensor data: {result.get('stderr', 'Unknown error')}"}
    
    return {"success": False, "error": f"Unknown hardware command: {command}"}

def handle_screen_interaction(command: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle screen interaction commands"""
    
    if command == 'tap':
        x = params.get('x')
        y = params.get('y')
        
        if x is None or y is None:
            return {"success": False, "error": "Parameters 'x' and 'y' are required"}
        
        result = mcp_server._execute_adb_command(['shell', 'input', 'tap', str(x), str(y)])
        
        if result['success']:
            return {"success": True, "message": f"Tapped at coordinates ({x}, {y})"}
        else:
            return {"success": False, "error": f"Failed to tap: {result.get('stderr', 'Unknown error')}"}
    
    elif command == 'longPress':
        x = params.get('x')
        y = params.get('y')
        duration_ms = params.get('durationMs')
        
        if x is None or y is None or duration_ms is None:
            return {"success": False, "error": "Parameters 'x', 'y', and 'durationMs' are required"}
        
        # ADB input doesn't have direct long press, simulate with swipe of same coordinates
        result = mcp_server._execute_adb_command([
            'shell', 'input', 'swipe', str(x), str(y), str(x), str(y), str(duration_ms)
        ])
        
        if result['success']:
            return {"success": True, "message": f"Long pressed at ({x}, {y}) for {duration_ms}ms"}
        else:
            return {"success": False, "error": f"Failed to long press: {result.get('stderr', 'Unknown error')}"}
    
    elif command == 'swipe':
        start_x = params.get('startX')
        start_y = params.get('startY')
        end_x = params.get('endX')
        end_y = params.get('endY')
        duration_ms = params.get('durationMs')
        
        required_params = [start_x, start_y, end_x, end_y, duration_ms]
        if any(param is None for param in required_params):
            return {"success": False, "error": "Parameters 'startX', 'startY', 'endX', 'endY', and 'durationMs' are required"}
        
        result = mcp_server._execute_adb_command([
            'shell', 'input', 'swipe', str(start_x), str(start_y), str(end_x), str(end_y), str(duration_ms)
        ])
        
        if result['success']:
            return {"success": True, "message": f"Swiped from ({start_x}, {start_y}) to ({end_x}, {end_y}) in {duration_ms}ms"}
        else:
            return {"success": False, "error": f"Failed to swipe: {result.get('stderr', 'Unknown error')}"}
    
    return {"success": False, "error": f"Unknown screen interaction command: {command}"}

def handle_system_settings(command: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle system settings commands"""
    
    if command == 'getSystemSetting':
        key = params.get('key')
        if not key:
            return {"success": False, "error": "Parameter 'key' is required"}
        
        result = mcp_server._execute_adb_command(['shell', 'settings', 'get', 'system', key])
        
        if result['success']:
            value = result['stdout'].strip()
            return {"success": True, "key": key, "value": value}
        else:
            return {"success": False, "error": f"Failed to get setting: {result.get('stderr', 'Unknown error')}"}
    
    elif command == 'setSystemSetting':
        key = params.get('key')
        value = params.get('value')
        
        if not key or value is None:
            return {"success": False, "error": "Parameters 'key' and 'value' are required"}
        
        result = mcp_server._execute_adb_command(['shell', 'settings', 'put', 'system', key, str(value)])
        
        if result['success']:
            return {"success": True, "message": f"Set {key} = {value}"}
        else:
            return {"success": False, "error": f"Failed to set setting: {result.get('stderr', 'Unknown error')}"}
    
    return {"success": False, "error": f"Unknown system settings command: {command}"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)