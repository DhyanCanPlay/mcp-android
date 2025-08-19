#!/bin/bash

# MCP Android Server Setup Script
# This script helps set up the environment for the MCP Android Server

set -e

echo "🤖 MCP Android Server Setup"
echo "=========================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

echo "✅ pip found"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if ADB is installed
if ! command -v adb &> /dev/null; then
    echo "⚠️  ADB not found. Please install Android SDK platform-tools."
    echo "   On Ubuntu/Debian: sudo apt-get install android-tools-adb"
    echo "   On macOS: brew install android-platform-tools"
    echo "   Or download from: https://developer.android.com/studio/releases/platform-tools"
else
    echo "✅ ADB found: $(adb version | head -n1)"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the server:"
echo "  python3 mcp_server.py"
echo ""
echo "To test with an Android device:"
echo "  1. Enable Developer Options on your Android device"
echo "  2. Enable USB Debugging"
echo "  3. Connect via USB and authorize the computer"
echo "  4. Verify connection: adb devices"
echo ""