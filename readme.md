# 🤖 MCP Android Server

<p align="center">
  <em>A Model Context Protocol (MCP) server for AI-driven Android device control</em>
</p>

---

## 🚀 About The Project

A comprehensive server implementing the Model Context Protocol (MCP) to enable AI agents to intelligently control and interact with Android devices. This server provides three main modules for complete device control:

- **HardwareControl**: WiFi, Bluetooth, Torch, and Sensor management
- **ScreenInteraction**: Touch gestures, taps, swipes, and long presses
- **SystemSettings**: Read and modify system configuration

## ✨ Features

### Hardware Control
- ✅ WiFi enable/disable
- ✅ Bluetooth enable/disable  
- ✅ Camera torch/flashlight control
- ✅ Sensor data retrieval (accelerometer, gyroscope, GPS, etc.)

### Screen Interaction
- ✅ Precise tap gestures at coordinates
- ✅ Long press with customizable duration
- ✅ Swipe gestures with start/end coordinates

### System Settings
- ✅ Read system settings (brightness, timeout, etc.)
- ✅ Modify system settings (requires appropriate permissions)

## 🛠️ Installation

### Prerequisites
- Python 3.7+
- Android Debug Bridge (ADB)
- Android device with USB debugging enabled

### Setup
1. Clone the repository:
```bash
git clone https://github.com/DhyanCanPlay/mcp-android.git
cd mcp-android
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Connect your Android device and enable USB debugging

4. Start the server:
```bash
python3 server.py
# or use the convenience script
./start_server.sh
```

## 📖 API Usage

The server runs on `http://localhost:5000` by default and accepts POST requests at `/mcp/command`.

### Request Format
```json
{
  "command": "commandName",
  "params": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

### Example Commands

#### Hardware Control
```bash
# Enable WiFi
curl -X POST http://localhost:5000/mcp/command \
  -H "Content-Type: application/json" \
  -d '{"command": "setWifiState", "params": {"state": true}}'

# Turn on torch
curl -X POST http://localhost:5000/mcp/command \
  -H "Content-Type: application/json" \
  -d '{"command": "setTorchState", "params": {"state": true, "brightnessLevel": 80}}'

# Get sensor data
curl -X POST http://localhost:5000/mcp/command \
  -H "Content-Type: application/json" \
  -d '{"command": "getSensorData", "params": {"sensorType": "accelerometer"}}'
```

#### Screen Interaction
```bash
# Tap at coordinates
curl -X POST http://localhost:5000/mcp/command \
  -H "Content-Type: application/json" \
  -d '{"command": "tap", "params": {"x": 540, "y": 1350}}'

# Swipe gesture
curl -X POST http://localhost:5000/mcp/command \
  -H "Content-Type: application/json" \
  -d '{"command": "swipe", "params": {"startX": 500, "startY": 1500, "endX": 500, "endY": 500, "durationMs": 200}}'
```

#### System Settings
```bash
# Get screen brightness
curl -X POST http://localhost:5000/mcp/command \
  -H "Content-Type: application/json" \
  -d '{"command": "getSystemSetting", "params": {"key": "screen_brightness"}}'

# Set screen timeout
curl -X POST http://localhost:5000/mcp/command \
  -H "Content-Type: application/json" \
  -d '{"command": "setSystemSetting", "params": {"key": "screen_off_timeout", "value": "60000"}}'
```

## 🧪 Testing

Run the test suite to verify functionality:
```bash
python3 test_server.py
```

Check server health:
```bash
curl http://localhost:5000/health
```

## ⚙️ Configuration

Edit `config.json` to customize server settings:
```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": true
  },
  "android": {
    "adb_timeout": 30,
    "default_device": null
  }
}
```

## 🔧 Requirements

- Android device with USB debugging enabled
- ADB installed and accessible in PATH
- Python dependencies (see requirements.txt)

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---
