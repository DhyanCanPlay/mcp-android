#!/bin/bash

# MCP Android Server Installation Script

echo "🤖 MCP Android Server Setup"
echo "============================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is required but not installed."
    echo "Please install Python 3.7+ and try again."
    exit 1
fi

echo "✅ Python3 found"

# Check ADB
if ! command -v adb &> /dev/null; then
    echo "⚠️  ADB (Android Debug Bridge) not found in PATH"
    echo "   You can install it via:"
    echo "   - Ubuntu/Debian: sudo apt install android-tools-adb"
    echo "   - macOS: brew install android-platform-tools"
    echo "   - Windows: Download Android SDK Platform Tools"
    echo ""
    echo "   The server will still work but Android commands will fail."
else
    echo "✅ ADB found"
fi

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Next steps:"
echo "1. Connect your Android device via USB"
echo "2. Enable USB debugging on your device"
echo "3. Run: python3 server.py"
echo "4. Test with: python3 example_client.py"
echo ""
echo "The server will be available at: http://localhost:5000"