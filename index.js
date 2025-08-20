import { FastMCP } from 'fastmcp';
import { exec } from 'child_process';
import { z } from 'zod';

// Helper function to execute shell commands
function executeCommand(command) {
    return new Promise((resolve, reject) => {
        exec(command, (error, stdout, stderr) => {
            if (error) {
                console.error(`Exec Error: ${error.message}`);
                reject(error);
                return;
            }
            if (stderr) {
                console.warn(`Stderr: ${stderr}`);
            }
            resolve(stdout);
        });
    });
}


// 1. Create the server
const server = new FastMCP({
    name: "TARA ADB Control Server",
    version: "3.1.0 (fastmcp-only)",
});

// 2. Add your tools
//wifi_control
server.addTool({
    name: 'wifi_control',
    description: 'Turns the WiFi on or off on a connected Android device using ADB.',
    parameters: z.object({
        state: z.enum(['on', 'off']).describe("The desired WiFi state. Can be 'on' or 'off'."),
    }),
    execute: async ({ state }) => {
        const adbCommand = state === 'on'
            ? 'adb shell svc wifi enable'
            : 'adb shell svc wifi disable';
        try {
            await executeCommand(adbCommand);
            return `Successfully turned WiFi ${state}.`;
        } catch (error) {
            return `ADB command failed: ${error.message}`;
        }
    },
});

//device list
server.addTool({
    name: 'device_list',
    description: 'Lists all connected Android devices using ADB.',
    parameters: z.object({}),
    execute: async () => {
        const adbCommand = 'adb devices';
        try {
            const output = await executeCommand(adbCommand);
            return `Connected devices:\n${output}`;
        } catch (error) {
            return `ADB command failed: ${error.message}`;
        }
    },
});



// Bluetooth Control
server.addTool({
    name: 'bt_control',
    description: 'Turns the Bluetooth on or off on a connected Android device using ADB.',
    parameters: z.object({
        state: z.enum(['on', 'off']).describe("The desired Bluetooth state. Can be 'on' or 'off'."),
    }),
    execute: async ({ state }) => {
        const adbCommand = state === 'on'
            ? 'adb shell svc bluetooth enable'
            : 'adb shell svc bluetooth disable';
        try {
            await executeCommand(adbCommand);
            return `Successfully turned Bluetooth ${state}.`;
        } catch (error) {
            return `ADB command failed: ${error.message}`;
        }
    },
});
// Volume Control
server.addTool({
    name: 'volume_control',
    description: 'Controls the volume on a connected Android device using ADB.',
    parameters: z.object({
        action: z.enum(['increase', 'decrease', 'mute']).describe("The volume action to perform."),
    }),
    execute: async ({ action }) => {
        // Map actions to ADB keyevents
        const keyeventMap = {
            increase: 24,     
            decrease: 25,    
            mute: 164,
        };
        const keyevent = keyeventMap[action];
        if (!keyevent) {f
            return `Unsupported action: ${action}`;
        }
        const adbCommand = `adb shell input keyevent ${keyevent}`;
        try {
            await executeCommand(adbCommand);
            return `Successfully performed ${action} action on music playback.`;
        } catch (error) {
            return `ADB command failed: ${error.message}`;
        }
    },
});
                
// Music Control
server.addTool({
    name: 'music_control',
    description: 'Controls music playback on a connected Android device using ADB keyevents.',
    parameters: z.object({
        action: z.enum(['play', 'pause', 'next', 'previous', 'resume', 'stop']).describe("The music playback action to perform."),
    }),
    execute: async ({ action }) => {
        // Map actions to ADB keyevents
        const keyeventMap = {
            play: 126,     // Play resume
            pause: 127,    // Pause playback
            next: 87,      // Next song
            previous: 88,  // Previous song
            resume: 126,   // Resume playback
            stop: 86       // Stop play
        };
        const keyevent = keyeventMap[action];
        if (!keyevent) {f
            return `Unsupported action: ${action}`;
        }
        const adbCommand = `adb shell input keyevent ${keyevent}`;
        try {
            await executeCommand(adbCommand);
            return `Successfully performed ${action} action on music playback.`;
        } catch (error) {
            return `ADB command failed: ${error.message}`;
        }
    },
});

// 3. Start the server
const PORT = 3000;
server.start({
    transportType: "httpStream",
    httpStream: {
        port: PORT,
    },
});
console.log(`🚀 TARA's fastmcp server is now running on http://localhost:${PORT}/mcp`);