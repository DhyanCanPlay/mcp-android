# This file will contain the logic to interact with the Android device using ADB.
import subprocess

def execute_adb_command(command):
    """Executes an ADB command and returns the output."""
    try:
        result = subprocess.run(
            f"adb {command}",
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip(), None
    except subprocess.CalledProcessError as e:
        return None, e.stderr.strip()

def handle_tap(x, y):
    """Handles the tap command."""
    return execute_adb_command(f"shell input tap {x} {y}")

def handle_swipe(x1, y1, x2, y2, duration):
    """Handles the swipe command."""
    return execute_adb_command(f"shell input swipe {x1} {y1} {x2} {y2} {duration}")

def handle_type(text):
    """Handles the type command."""
    return execute_adb_command(f"shell input text '{text}'")
