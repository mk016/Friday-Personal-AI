import logging
import subprocess
import os
import platform
from livekit.agents import function_tool, RunContext

def is_mac():
    """Check if running on Mac"""
    return platform.system() == "Darwin"

@function_tool()
async def execute_mac_command(
    context: RunContext,  # type: ignore
    command: str
) -> str:
    """
    Execute Mac system commands like controlling brightness, volume, opening apps etc.
    Args:
        command: The command to execute (e.g. "increase brightness", "open safari", etc.)
    """
    if not is_mac():
        return "Mac control features are only available on macOS."
    
    command = command.lower()
    
    try:
        # Brightness controls
        if "increase brightness" in command or "brightness up" in command:
            script = '''
            tell application "System Events"
                set currentBrightness to brightness of (first display)
                set newBrightness to currentBrightness + 0.2
                if newBrightness > 1 then set newBrightness to 1
                set brightness of (first display) to newBrightness
            end tell
            '''
            subprocess.run(["osascript", "-e", script], check=True)
            return "Screen brightness increased"
        
        elif "decrease brightness" in command or "brightness down" in command:
            script = '''
            tell application "System Events"
                set currentBrightness to brightness of (first display)
                set newBrightness to currentBrightness - 0.2
                if newBrightness < 0 then set newBrightness to 0
                set brightness of (first display) to newBrightness
            end tell
            '''
            subprocess.run(["osascript", "-e", script], check=True)
            return "Screen brightness decreased"
        
        # Volume controls
        elif "increase volume" in command or "volume up" in command:
            script = 'set volume output volume (output volume of (get volume settings) + 1)'
            subprocess.run(["osascript", "-e", script], check=True)
            return "Volume increased"
        
        elif "decrease volume" in command or "volume down" in command:
            script = 'set volume output volume (output volume of (get volume settings) - 1)'
            subprocess.run(["osascript", "-e", script], check=True)
            return "Volume decreased"
        
        elif "mute" in command or "mute volume" in command:
            script = 'set volume with output muted'
            subprocess.run(["osascript", "-e", script], check=True)
            return "Volume muted"
        
        # Folder commands
        elif "open downloads" in command:
            downloads_path = os.path.expanduser("~/Downloads")
            subprocess.run(["open", downloads_path])
            return "Opened Downloads folder in Finder"
        
        elif "open desktop" in command:
            desktop_path = os.path.expanduser("~/Desktop")
            subprocess.run(["open", desktop_path])
            return "Opened Desktop folder in Finder"
        
        elif "open documents" in command:
            documents_path = os.path.expanduser("~/Documents")
            subprocess.run(["open", documents_path])
            return "Opened Documents folder in Finder"
        
        # Browser commands
        elif "open safari" in command:
            subprocess.run(["open", "-a", "Safari"])
            return "Opened Safari browser"
        
        elif "open chrome" in command:
            subprocess.run(["open", "-a", "Google Chrome"])
            return "Opened Google Chrome browser"
        
        elif "open browser" in command:
            subprocess.run(["open", "-a", "Safari"])
            return "Opened default web browser"
        
        # Application commands
        elif "open finder" in command:
            subprocess.run(["open", "-a", "Finder"])
            return "Opened Finder"
        
        elif "open terminal" in command:
            subprocess.run(["open", "-a", "Terminal"])
            return "Opened Terminal"
        
        elif "open calculator" in command:
            subprocess.run(["open", "-a", "Calculator"])
            return "Opened Calculator"
        
        elif "open calendar" in command:
            subprocess.run(["open", "-a", "Calendar"])
            return "Opened Calendar"
        
        elif "open notes" in command:
            subprocess.run(["open", "-a", "Notes"])
            return "Opened Notes"
        
        elif "open system preferences" in command:
            subprocess.run(["open", "-a", "System Preferences"])
            return "Opened System Preferences"
        
        elif "open activity monitor" in command:
            subprocess.run(["open", "-a", "Activity Monitor"])
            return "Opened Activity Monitor"
        
        # System commands
        elif "take screenshot" in command:
            desktop_path = os.path.expanduser("~/Desktop")
            timestamp = subprocess.check_output(["date", "+%Y%m%d_%H%M%S"]).decode().strip()
            filename = f"Screenshot_{timestamp}.png"
            filepath = os.path.join(desktop_path, filename)
            subprocess.run(["screencapture", filepath])
            return f"Screenshot saved to Desktop as {filename}"
        
        elif "lock screen" in command:
            script = 'tell application "System Events" to keystroke "q" using {command down, control down}'
            subprocess.run(["osascript", "-e", script])
            return "Screen locked"
        
        elif "empty trash" in command:
            script = '''
            tell application "Finder"
                empty trash
            end tell
            '''
            subprocess.run(["osascript", "-e", script])
            return "Trash emptied successfully"
        
        else:
            return None  # No Mac command recognized
            
    except Exception as e:
        return f"Failed to execute command: {e}"

@function_tool()
async def set_brightness(
    context: RunContext,  # type: ignore
    level: int
) -> str:
    """
    Set screen brightness level (0-100) on Mac.
    """
    if not is_mac():
        return "This function is only supported on macOS."
    try:
        if not 0 <= level <= 100:
            return "Brightness level must be between 0 and 100."
        
        # Convert to AppleScript brightness scale (0.0 to 1.0)
        brightness_value = level / 100.0
        script = f'tell application "System Events" to set brightness of (first display) to {brightness_value}'
        subprocess.run(["osascript", "-e", script], check=True)
        return f"Screen brightness set to {level}%"
    except Exception as e:
        logging.error(f"Error setting brightness: {e}")
        return f"Failed to set brightness: {e}"

@function_tool()
async def set_volume(
    context: RunContext,  # type: ignore
    level: int
) -> str:
    """
    Set system volume level (0-100) on Mac.
    """
    if not is_mac():
        return "This function is only supported on macOS."
    try:
        if not 0 <= level <= 100:
            return "Volume level must be between 0 and 100."
        
        # Convert to AppleScript volume scale (0-7)
        volume_value = int((level / 100) * 7)
        script = f'set volume output volume {volume_value}'
        subprocess.run(["osascript", "-e", script], check=True)
        return f"Volume set to {level}%"
    except Exception as e:
        logging.error(f"Error setting volume: {e}")
        return f"Failed to set volume: {e}"

@function_tool()
async def take_screenshot(
    context: RunContext,  # type: ignore
    save_to_desktop: bool = True
) -> str:
    """
    Take a screenshot on Mac.
    """
    if not is_mac():
        return "This function is only supported on macOS."
    try:
        if save_to_desktop:
            desktop_path = os.path.expanduser("~/Desktop")
            timestamp = subprocess.check_output(["date", "+%Y%m%d_%H%M%S"]).decode().strip()
            filename = f"Screenshot_{timestamp}.png"
            filepath = os.path.join(desktop_path, filename)
            subprocess.run(["screencapture", filepath])
            return f"Screenshot saved to Desktop as {filename}"
        else:
            subprocess.run(["screencapture", "-c"])  # Save to clipboard
            return "Screenshot saved to clipboard"
    except Exception as e:
        logging.error(f"Error taking screenshot: {e}")
        return f"Failed to take screenshot: {e}"

@function_tool()
async def lock_screen(
    context: RunContext,  # type: ignore
) -> str:
    """
    Lock the Mac screen.
    """
    if not is_mac():
        return "This function is only supported on macOS."
    try:
        script = 'tell application "System Events" to keystroke "q" using {command down, control down}'
        subprocess.run(["osascript", "-e", script])
        return "Screen locked"
    except Exception as e:
        logging.error(f"Error locking screen: {e}")
        return f"Failed to lock screen: {e}"

@function_tool()
async def empty_trash(
    context: RunContext,  # type: ignore
) -> str:
    """
    Empty the Trash on Mac.
    """
    if not is_mac():
        return "This function is only supported on macOS."
    try:
        script = '''
        tell application "Finder"
            empty trash
        end tell
        '''
        subprocess.run(["osascript", "-e", script])
        return "Trash emptied successfully"
    except Exception as e:
        logging.error(f"Error emptying trash: {e}")
        return f"Failed to empty trash: {e}" 