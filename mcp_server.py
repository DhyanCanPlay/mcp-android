#!/usr/bin/env python3
"""
MCP Android Server - A Model Context Protocol server for Android device control.

This server implements basic Android device control capabilities including:
- tap: Tap at specific coordinates
- swipe: Swipe between two points
- type: Type text into the current input field
"""

import asyncio
import json
import logging
import subprocess
import sys
from typing import Dict, List, Optional, Any
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Pydantic models for request/response
class TapRequest(BaseModel):
    x: int = Field(..., description="X coordinate for tap")
    y: int = Field(..., description="Y coordinate for tap")
    device_id: Optional[str] = Field(None, description="Device ID (optional)")

class SwipeRequest(BaseModel):
    start_x: int = Field(..., description="Starting X coordinate")
    start_y: int = Field(..., description="Starting Y coordinate")
    end_x: int = Field(..., description="Ending X coordinate")
    end_y: int = Field(..., description="Ending Y coordinate")
    duration: int = Field(300, description="Swipe duration in milliseconds")
    device_id: Optional[str] = Field(None, description="Device ID (optional)")

class TypeRequest(BaseModel):
    text: str = Field(..., description="Text to type")
    device_id: Optional[str] = Field(None, description="Device ID (optional)")

class MCPResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class AndroidController:
    """Handles Android device communication via ADB."""
    
    def __init__(self):
        self.devices = []
        self.refresh_devices()
    
    def _run_adb_command(self, command: List[str], device_id: Optional[str] = None) -> str:
        """Execute ADB command and return output."""
        if device_id:
            cmd = ["adb", "-s", device_id] + command
        else:
            cmd = ["adb"] + command
        
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=True,
                timeout=10
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"ADB command failed: {' '.join(cmd)}, Error: {e.stderr}")
            raise HTTPException(status_code=500, detail=f"ADB command failed: {e.stderr}")
        except subprocess.TimeoutExpired:
            logger.error(f"ADB command timed out: {' '.join(cmd)}")
            raise HTTPException(status_code=500, detail="ADB command timed out")
    
    def refresh_devices(self) -> List[str]:
        """Get list of connected Android devices."""
        try:
            output = self._run_adb_command(["devices"])
            lines = output.split('\n')[1:]  # Skip header line
            self.devices = []
            
            for line in lines:
                if line.strip() and '\tdevice' in line:
                    device_id = line.split('\t')[0]
                    self.devices.append(device_id)
            
            logger.info(f"Found {len(self.devices)} connected devices: {self.devices}")
            return self.devices
        except Exception as e:
            logger.error(f"Failed to refresh devices: {e}")
            self.devices = []
            return []
    
    def get_default_device(self) -> Optional[str]:
        """Get the default device (first available device)."""
        if not self.devices:
            self.refresh_devices()
        return self.devices[0] if self.devices else None
    
    def tap(self, x: int, y: int, device_id: Optional[str] = None) -> bool:
        """Perform a tap at the specified coordinates."""
        device = device_id or self.get_default_device()
        if not device:
            raise HTTPException(status_code=404, detail="No Android devices connected")
        
        try:
            self._run_adb_command(["shell", "input", "tap", str(x), str(y)], device)
            logger.info(f"Tapped at ({x}, {y}) on device {device}")
            return True
        except Exception as e:
            logger.error(f"Failed to tap at ({x}, {y}): {e}")
            raise
    
    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, 
              duration: int = 300, device_id: Optional[str] = None) -> bool:
        """Perform a swipe gesture between two points."""
        device = device_id or self.get_default_device()
        if not device:
            raise HTTPException(status_code=404, detail="No Android devices connected")
        
        try:
            self._run_adb_command([
                "shell", "input", "swipe", 
                str(start_x), str(start_y), str(end_x), str(end_y), str(duration)
            ], device)
            logger.info(f"Swiped from ({start_x}, {start_y}) to ({end_x}, {end_y}) on device {device}")
            return True
        except Exception as e:
            logger.error(f"Failed to swipe: {e}")
            raise
    
    def type_text(self, text: str, device_id: Optional[str] = None) -> bool:
        """Type text into the current input field."""
        device = device_id or self.get_default_device()
        if not device:
            raise HTTPException(status_code=404, detail="No Android devices connected")
        
        try:
            # Escape special characters for shell
            escaped_text = text.replace(' ', '%s').replace('&', r'\&').replace('<', r'\<').replace('>', r'\>')
            self._run_adb_command(["shell", "input", "text", escaped_text], device)
            logger.info(f"Typed text '{text}' on device {device}")
            return True
        except Exception as e:
            logger.error(f"Failed to type text '{text}': {e}")
            raise

# Initialize FastAPI app and Android controller
app = FastAPI(
    title="MCP Android Server",
    description="Model Context Protocol server for Android device control",
    version="1.0.0"
)

android_controller = AndroidController()

@app.get("/", response_model=MCPResponse)
async def root():
    """Root endpoint with server information."""
    return MCPResponse(
        success=True,
        message="MCP Android Server is running",
        data={
            "version": "1.0.0",
            "supported_commands": ["tap", "swipe", "type"],
            "connected_devices": android_controller.devices
        }
    )

@app.get("/devices", response_model=MCPResponse)
async def get_devices():
    """Get list of connected Android devices."""
    devices = android_controller.refresh_devices()
    return MCPResponse(
        success=True,
        message=f"Found {len(devices)} connected devices",
        data={"devices": devices}
    )

@app.post("/tap", response_model=MCPResponse)
async def tap(request: TapRequest):
    """Perform a tap gesture at specified coordinates."""
    try:
        android_controller.tap(request.x, request.y, request.device_id)
        return MCPResponse(
            success=True,
            message=f"Successfully tapped at ({request.x}, {request.y})",
            data={"x": request.x, "y": request.y, "device_id": request.device_id}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in tap: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/swipe", response_model=MCPResponse)
async def swipe(request: SwipeRequest):
    """Perform a swipe gesture between two points."""
    try:
        android_controller.swipe(
            request.start_x, request.start_y, 
            request.end_x, request.end_y, 
            request.duration, request.device_id
        )
        return MCPResponse(
            success=True,
            message=f"Successfully swiped from ({request.start_x}, {request.start_y}) to ({request.end_x}, {request.end_y})",
            data={
                "start_x": request.start_x, "start_y": request.start_y,
                "end_x": request.end_x, "end_y": request.end_y,
                "duration": request.duration, "device_id": request.device_id
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in swipe: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/type", response_model=MCPResponse)
async def type_text(request: TypeRequest):
    """Type text into the current input field."""
    try:
        android_controller.type_text(request.text, request.device_id)
        return MCPResponse(
            success=True,
            message=f"Successfully typed text: {request.text}",
            data={"text": request.text, "device_id": request.device_id}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in type: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=MCPResponse)
async def health_check():
    """Health check endpoint."""
    try:
        # Check if ADB is available
        subprocess.run(["adb", "version"], capture_output=True, check=True, timeout=5)
        devices = android_controller.refresh_devices()
        
        return MCPResponse(
            success=True,
            message="Server is healthy",
            data={
                "adb_available": True,
                "connected_devices": len(devices),
                "device_list": devices
            }
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return MCPResponse(
            success=False,
            message="ADB not available or not working",
            data={"adb_available": False, "connected_devices": 0}
        )

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="MCP Android Server")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--log-level", default="info", choices=["debug", "info", "warning", "error"])
    
    args = parser.parse_args()
    
    # Set log level
    logging.getLogger().setLevel(getattr(logging, args.log_level.upper()))
    
    logger.info(f"Starting MCP Android Server on {args.host}:{args.port}")
    
    # Check if ADB is available
    try:
        subprocess.run(["adb", "version"], capture_output=True, check=True)
        logger.info("ADB is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning("ADB not found. Please install Android SDK platform-tools.")
    
    # Start the server
    uvicorn.run(app, host=args.host, port=args.port, log_level=args.log_level)