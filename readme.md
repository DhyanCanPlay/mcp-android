# 🤖 MCP Android Server

A server implementing the **Model Context Protocol (MCP)** to enable AI agents to intelligently control and interact with Android devices.

## ✨ Features

- **Remote Android Control**: Control Android devices via ADB (Android Debug Bridge)
- **RESTful API**: Simple HTTP API for device interactions
- **Core Commands**:
  - `tap`: Tap at specific coordinates
  - `swipe`: Swipe between two points  
  - `type`: Type text into input fields
- **Multi-device Support**: Control multiple connected Android devices
- **Health Monitoring**: Built-in health checks and device detection

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Android SDK Platform Tools (for ADB)
- Android device with USB debugging enabled

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/DhyanCanPlay/mcp-android.git
   cd mcp-android
   ```

2. **Run the setup script**:
   ```bash
   ./setup.sh
   ```

3. **Start the server**:
   ```bash
   python3 mcp_server.py
   ```

The server will start on `http://127.0.0.1:8000` by default.

## 📱 Android Device Setup

1. **Enable Developer Options**:
   - Go to Settings → About Phone
   - Tap "Build Number" 7 times

2. **Enable USB Debugging**:
   - Go to Settings → Developer Options
   - Enable "USB Debugging"

3. **Connect and Authorize**:
   - Connect your device via USB
   - Authorize the computer when prompted
   - Verify connection: `adb devices`

## 🔧 API Usage

### Health Check
```bash
curl http://127.0.0.1:8000/health
```

### Get Connected Devices
```bash
curl http://127.0.0.1:8000/devices
```

### Tap Command
```bash
curl -X POST http://127.0.0.1:8000/tap \
  -H "Content-Type: application/json" \
  -d '{"x": 500, "y": 500}'
```

### Swipe Command
```bash
curl -X POST http://127.0.0.1:8000/swipe \
  -H "Content-Type: application/json" \
  -d '{"start_x": 300, "start_y": 800, "end_x": 700, "end_y": 800, "duration": 500}'
```

### Type Text Command
```bash
curl -X POST http://127.0.0.1:8000/type \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World!"}'
```

## 🧪 Testing

Run the example client to test all commands:

```bash
python3 example_client.py
```

## 📖 API Documentation

Once the server is running, visit `http://127.0.0.1:8000/docs` for interactive API documentation powered by FastAPI.

## 🛠️ Command Line Options

```bash
python3 mcp_server.py --help
```

Options:
- `--host`: Host to bind to (default: 127.0.0.1)
- `--port`: Port to bind to (default: 8000)
- `--log-level`: Logging level (debug, info, warning, error)

## 🔍 Troubleshooting

### ADB Not Found
```bash
# Ubuntu/Debian
sudo apt-get install android-tools-adb

# macOS
brew install android-platform-tools
```

### No Devices Found
- Ensure USB debugging is enabled
- Check USB connection
- Run `adb devices` to verify device recognition
- Try different USB ports/cables

### Permission Denied
- Ensure the computer is authorized on the Android device
- Try revoking and re-authorizing USB debugging

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.
