import logging
import subprocess
import os
import platform
from livekit.agents import function_tool, RunContext

def is_mac():
    """Check if running on Mac"""
    return platform.system() == "Darwin"

@function_tool()
async def open_app(
    context: RunContext,  # type: ignore
    app_name: str
) -> str:
    """
    Open applications on Mac like Safari, Chrome, Calculator, etc.
    Args:
        app_name: Name of the application to open (e.g., 'safari', 'chrome', 'calculator')
    """
    if not is_mac():
        return "This function is only supported on macOS."
    
    # Map common app names to their actual application names
    app_mapping = {
        'safari': 'Safari',
        'chrome': 'Google Chrome',
        'calculator': 'Calculator',
        'calendar': 'Calendar',
        'mail': 'Mail',
        'notes': 'Notes',
        'finder': 'Finder',
        'terminal': 'Terminal',
        'system preferences': 'System Preferences',
        'activity monitor': 'Activity Monitor',
        'textedit': 'TextEdit',
        'preview': 'Preview',
        'music': 'Music',
        'photos': 'Photos',
        'messages': 'Messages',
        'facetime': 'FaceTime'
    }
    
    actual_app_name = app_mapping.get(app_name.lower(), app_name)
    
    try:
        result = subprocess.run(
            ["open", "-a", actual_app_name], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if result.returncode == 0:
            return f"✅ {actual_app_name} opened successfully / {actual_app_name} खोला गया"
        else:
            return f"❌ Application '{actual_app_name}' not found. Please check if it's installed."
            
    except Exception as e:
        logging.error(f"Error opening app {app_name}: {e}")
        return f"❌ Error opening {actual_app_name}: {str(e)}"

@function_tool()
async def close_application(
    context: RunContext,  # type: ignore
    app_name: str
) -> str:
    """
    Close any application on Mac (Chrome, Safari, Finder, etc.).
    Args:
        app_name: Name of application to close (chrome, safari, finder, etc.)
    """
    try:
        logging.info(f"Closing application: {app_name}")
        
        if not is_mac():
            return "यह फीचर केवल Mac पर उपलब्ध है। / This feature is only available on Mac."
        
        # Map common app names to actual app names
        app_mapping = {
            "chrome": "Google Chrome",
            "safari": "Safari", 
            "firefox": "Firefox",
            "finder": "Finder",
            "mail": "Mail",
            "music": "Music",
            "spotify": "Spotify",
            "whatsapp": "WhatsApp",
            "facetime": "FaceTime",
            "calendar": "Calendar",
            "notes": "Notes",
            "messages": "Messages",
            "photos": "Photos",
            "maps": "Maps"
        }
        
        actual_app_name = app_mapping.get(app_name.lower(), app_name.title())
        
        # AppleScript to close application
        applescript = f'''
        try
            tell application "{actual_app_name}"
                quit
            end tell
            return "Application closed successfully"
        on error errorMessage
            -- If quit doesn't work, force quit
            try
                tell application "System Events"
                    tell process "{actual_app_name}"
                        click menu item "Quit {actual_app_name}" of menu "File" of menu bar 1
                    end tell
                end tell
                return "Application force closed"
            on error
                return "Could not close application"
            end try
        end try
        '''
        
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            if "successfully" in result.stdout or "force closed" in result.stdout:
                logging.info(f"Application closed successfully: {actual_app_name}")
                return f"✅ {actual_app_name} बंद कर दिया। / {actual_app_name} closed successfully."
            else:
                return f"❌ {actual_app_name} बंद करने में समस्या हुई।"
        else:
            return f"❌ Application close करने में समस्या: {result.stderr}"
            
    except Exception as e:
        logging.error(f"Error closing application: {e}")
        return f"Application बंद करने में error: {str(e)}"

@function_tool()
async def control_music(
    context: RunContext,  # type: ignore
    action: str,
    song_name: str = ""
) -> str:
    """
    Control music playback (play, pause, next, previous, play specific song).
    Args:
        action: Action to perform (play, pause, next, previous, stop, play_song)
        song_name: Name of song to play (if action is play_song)
    """
    try:
        logging.info(f"Music control: {action} {song_name}")
        
        if not is_mac():
            return "यह फीचर केवल Mac पर उपलब्ध है। / This feature is only available on Mac."
        
        if action == "play_song" and song_name:
            # Search and play specific song
            applescript = f'''
            try
                tell application "Music"
                    activate
                    delay 1
                    
                    -- Search for the song
                    set searchResults to (search playlist "Library" for "{song_name}")
                    
                    if (count of searchResults) > 0 then
                        play (item 1 of searchResults)
                        return "Playing: {song_name}"
                    else
                        -- Try Spotify if available
                        tell application "Spotify"
                            activate
                            delay 1
                            play track "{song_name}"
                            return "Playing on Spotify: {song_name}"
                        end tell
                    end if
                end tell
            on error
                -- Fallback to media keys
                tell application "System Events"
                    key code 49  -- Space key (play/pause)
                end tell
                return "Media control executed"
            end try
            '''
        else:
            # Basic music controls
            action_commands = {
                "play": '''
                    try
                        tell application "Music"
                            play
                        end tell
                    on error
                        tell application "System Events"
                            key code 49  -- Space (play/pause)
                        end tell
                    end try
                ''',
                "pause": '''
                    try
                        tell application "Music"
                            pause
                        end tell
                    on error
                        tell application "System Events"
                            key code 49  -- Space (play/pause)
                        end tell
                    end try
                ''',
                "stop": '''
                    try
                        tell application "Music"
                            stop
                        end tell
                    on error
                        tell application "System Events"
                            key code 49  -- Space (play/pause)
                        end tell
                    end try
                ''',
                "next": '''
                    try
                        tell application "Music"
                            next track
                        end tell
                    on error
                        tell application "System Events"
                            key code 124  -- Right arrow (next)
                        end tell
                    end try
                ''',
                "previous": '''
                    try
                        tell application "Music"
                            previous track
                        end tell
                    on error
                        tell application "System Events"
                            key code 123  -- Left arrow (previous)
                        end tell
                    end try
                '''
            }
            
            applescript = action_commands.get(action.lower(), action_commands["play"])
        
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=20)
        
        if result.returncode == 0:
            if action == "play_song":
                return f"🎵 Playing song: '{song_name}' / गाना बज रहा है: '{song_name}'"
            else:
                action_hindi = {
                    "play": "चालू",
                    "pause": "रोक दिया", 
                    "stop": "बंद",
                    "next": "अगला गाना",
                    "previous": "पिछला गाना"
                }
                return f"🎵 Music {action} - Done! / Music {action_hindi.get(action, action)} कर दिया!"
        else:
            # Try using media keys as fallback
            if action in ["play", "pause"]:
                subprocess.run(['osascript', '-e', 'tell application "System Events" to key code 49'], timeout=5)
                return f"🎵 Music play/pause button दबाया गया।"
            return f"❌ Music control में समस्या: {result.stderr}"
            
    except Exception as e:
        logging.error(f"Error controlling music: {e}")
        return f"Music control में error: {str(e)}" 