import logging
import subprocess
import os
import platform
from livekit.agents import function_tool, RunContext

def is_mac():
    """Check if running on Mac"""
    return platform.system() == "Darwin"

@function_tool()
async def set_volume_precise(
    context: RunContext,  # type: ignore
    percentage: int
) -> str:
    """
    Set system volume to exact percentage (0-100).
    Args:
        percentage: Volume percentage from 0 to 100
    """
    if not is_mac():
        return "Volume control केवल macOS पर उपलब्ध है।"
    
    try:
        # Validate percentage
        if percentage < 0:
            percentage = 0
        elif percentage > 100:
            percentage = 100
            
        # Convert to AppleScript volume scale (0-100)
        script = f'set volume output volume {percentage}'
        subprocess.run(["osascript", "-e", script], check=True)
        
        return f"✅ Volume set to {percentage}%"
        
    except Exception as e:
        logging.error(f"Error setting volume: {e}")
        return f"❌ Volume set करने में error: {str(e)}"

@function_tool()
async def set_brightness_precise(
    context: RunContext,  # type: ignore
    percentage: int
) -> str:
    """
    Set screen brightness to exact percentage (0-100).
    Args:
        percentage: Brightness percentage from 0 to 100
    """
    if not is_mac():
        return "Brightness control केवल macOS पर उपलब्ध है।"
    
    try:
        # Validate percentage
        if percentage < 0:
            percentage = 0
        elif percentage > 100:
            percentage = 100
            
        # Convert percentage to decimal (0.0 to 1.0)
        brightness_value = percentage / 100.0
        
        script = f'''
        tell application "System Events"
            tell appearance preferences
                set brightness of (first display whose type is "built-in") to {brightness_value}
            end tell
        end tell
        '''
        
        # Alternative method using brightness utility
        subprocess.run(["brightness", str(brightness_value)], check=False)
        
        return f"✅ Brightness set to {percentage}%"
        
    except Exception as e:
        # Try alternative method
        try:
            # Install brightness utility if not available
            result = subprocess.run(["which", "brightness"], capture_output=True, text=True)
            if result.returncode != 0:
                return f"❌ Brightness control के लिए 'brightness' utility install करें: brew install brightness"
                
            brightness_value = percentage / 100.0
            subprocess.run(["brightness", str(brightness_value)], check=True)
            return f"✅ Brightness set to {percentage}%"
            
        except Exception as e2:
            logging.error(f"Error setting brightness: {e2}")
            return f"❌ Brightness set करने में error. System Preferences → Security & Privacy → Accessibility में Terminal को access दें।"

@function_tool()
async def open_folder_in_app(
    context: RunContext,  # type: ignore
    folder_path: str,
    application: str = "finder"
) -> str:
    """
    Open any folder in specified application.
    Args:
        folder_path: Path to folder (e.g., ~/Downloads, ~/Desktop, /Applications)
        application: App to open with (finder, terminal, vscode, etc.)
    """
    if not is_mac():
        return "Folder opening केवल macOS पर उपलब्ध है।"
    
    try:
        # Expand user path
        expanded_path = os.path.expanduser(folder_path)
        
        # Check if folder exists
        if not os.path.exists(expanded_path):
            return f"❌ Folder नहीं मिला: {folder_path}"
            
        if not os.path.isdir(expanded_path):
            return f"❌ यह folder नहीं है: {folder_path}"
            
        application = application.lower()
        
        if application in ["finder", "default"]:
            subprocess.run(["open", expanded_path], check=True)
            return f"✅ Opened {folder_path} in Finder"
            
        elif application in ["terminal", "iterm"]:
            script = f'''
            tell application "Terminal"
                activate
                do script "cd '{expanded_path}'"
            end tell
            '''
            subprocess.run(["osascript", "-e", script], check=True)
            return f"✅ Opened {folder_path} in Terminal"
            
        elif application in ["vscode", "code", "vs code"]:
            subprocess.run(["code", expanded_path], check=True)
            return f"✅ Opened {folder_path} in VS Code"
            
        elif application in ["sublime", "sublime text"]:
            subprocess.run(["subl", expanded_path], check=True)
            return f"✅ Opened {folder_path} in Sublime Text"
            
        else:
            # Try to open with generic application
            subprocess.run(["open", "-a", application, expanded_path], check=True)
            return f"✅ Opened {folder_path} with {application}"
            
    except subprocess.CalledProcessError as e:
        return f"❌ Error opening folder: Application '{application}' not found या installed नहीं है"
    except Exception as e:
        logging.error(f"Error opening folder: {e}")
        return f"❌ Folder open करने में error: {str(e)}"

@function_tool()
async def change_wallpaper(
    context: RunContext,  # type: ignore
    image_path: str = "",
    search_query: str = ""
) -> str:
    """
    Change Mac wallpaper. Can use local image or search online.
    Args:
        image_path: Path to local image file (optional)
        search_query: Search query to find wallpaper online (optional)
    """
    if not is_mac():
        return "Wallpaper change केवल macOS पर उपलब्ध है।"
    
    try:
        if image_path:
            # Use local image
            expanded_path = os.path.expanduser(image_path)
            if not os.path.exists(expanded_path):
                return f"❌ Image file नहीं मिली: {image_path}"
                
            script = f'''
            tell application "System Events"
                tell every desktop
                    set picture to "{expanded_path}"
                end tell
            end tell
            '''
            subprocess.run(["osascript", "-e", script], check=True)
            return f"✅ Wallpaper changed to: {image_path}"
            
        elif search_query:
            # Search for wallpaper online using Unsplash
            return f"🔍 Searching for '{search_query}' wallpaper online... (Feature coming soon - manual download required for now)"
            
        else:
            # Open wallpaper settings
            script = '''
            tell application "System Preferences"
                activate
                set current pane to pane "com.apple.preference.desktopscreeneffect"
            end tell
            '''
            subprocess.run(["osascript", "-e", script], check=True)
            return "✅ Opened Desktop & Dock preferences for wallpaper selection"
            
    except Exception as e:
        logging.error(f"Error changing wallpaper: {e}")
        return f"❌ Wallpaper change करने में error: {str(e)}" 