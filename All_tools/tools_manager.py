import logging
import subprocess
import os
import platform
from livekit.agents import function_tool, RunContext
from typing import List

# Import all tools from individual files
from .search_internet import search_internet
from .get_current_news import get_current_news
from .get_weather_info import get_weather_info
from .ai_api_tools import ask_cloud_api_with_internet, ask_deepseek_with_internet
from .mac_system_control import (
    execute_mac_command, set_brightness, set_volume, 
    take_screenshot, lock_screen, empty_trash
)
from .application_control import open_app, close_application, control_music
from .file_management import (
    create_file, delete_file, read_file_content, write_file_content,
    create_folder, list_folder_contents, copy_file_or_folder, move_file_or_folder
)
from .communication_tools import send_email, send_whatsapp_message, make_phone_call
from .system_info_tools import get_system_info, check_mac_permissions, get_downloads_info
from .screen_monitoring import (
    get_screen_info, get_open_windows_info, get_browser_tabs_detailed
)
from .advanced_mac_control import (
    toggle_wifi, toggle_bluetooth, toggle_dark_mode,
    set_audio_output, start_screen_saver, set_keyboard_backlight
)
from .web_browser_tools import (
    open_website, search_in_browser, open_web_search, control_browser_music
)
from .calendar_reminder_tools import get_calendar_events, create_reminder
from .smart_home_tools import control_smart_home
from .file_search_tools import find_and_replace_in_file, search_in_files
from .language_tools import detect_language
from .advanced_system_tools import (
    set_volume_precise, set_brightness_precise, 
    open_folder_in_app, change_wallpaper
)
from .complex_ai_tools import enhanced_internet_query, multi_source_analysis
from .whatsapp_desktop_tools import send_whatsapp_desktop_message, get_whatsapp_contacts
from .screen_reading_tools import (
    read_screen_text, analyze_screen_content, 
    fill_input_field, get_active_application_info
)

# Import new screen monitoring tools
from .screen_monitoring_advanced import (
    read_screen_content, read_browser_tab_content, 
    monitor_active_application, find_text_on_screen
)

def is_mac():
    """Check if running on Mac"""
    return platform.system() == "Darwin"

@function_tool()
async def send_whatsapp_desktop_message(
    context: RunContext,  # type: ignore
    contact_name: str,
    message: str
) -> str:
    """
    Send WhatsApp message using WhatsApp Desktop app (not web).
    Args:
        contact_name: Name of the contact to send message to
        message: Message content to send
    """
    try:
        logging.info(f"Sending WhatsApp Desktop message to {contact_name}: {message}")
        
        if not is_mac():
            return "This feature is only available on macOS."
        
        # AppleScript for WhatsApp Desktop app
        applescript = f'''
        try
            tell application "WhatsApp"
                activate
                delay 2
            end tell
            
            tell application "System Events"
                tell process "WhatsApp"
                    -- Search for contact
                    keystroke "f" using {{command down}}
                    delay 1
                    keystroke "{contact_name}"
                    delay 2
                    key code 36  -- Enter key
                    delay 1
                    
                    -- Type and send message
                    keystroke "{message}"
                    delay 0.5
                    key code 36  -- Enter key to send
                    delay 0.5
                end tell
            end tell
            
            return "Message sent successfully"
            
        on error errorMessage
            return "Error: " & errorMessage
        end try
        '''
        
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0 and "successfully" in result.stdout:
            logging.info(f"WhatsApp Desktop message sent successfully to {contact_name}")
            return f"WhatsApp Desktop message sent to {contact_name}: '{message}'"
        else:
            # Fallback - open WhatsApp Desktop
            subprocess.run(['open', '-a', 'WhatsApp'], timeout=10)
            return f"WhatsApp Desktop opened. Please manually send message to {contact_name}: '{message}'"
            
    except Exception as e:
        logging.error(f"Error sending WhatsApp Desktop message: {e}")
        return f"Error sending WhatsApp Desktop message: {str(e)}"

@function_tool()
async def get_whatsapp_contacts(
    context: RunContext,  # type: ignore
) -> str:
    """
    Get list of recent WhatsApp contacts.
    """
    try:
        logging.info("Getting WhatsApp contacts")
        
        if not is_mac():
            return "This feature is only available on macOS."
        
        # AppleScript to get recent contacts
        applescript = '''
        try
            tell application "WhatsApp"
                activate
                delay 2
            end tell
            
            tell application "System Events"
                tell process "WhatsApp"
                    -- Get recent chats
                    keystroke "1" using {command down}
                    delay 1
                    
                    -- This would need more complex implementation
                    -- For now, just return that WhatsApp is open
                    return "WhatsApp opened - recent contacts visible"
                end tell
            end tell
            
        on error errorMessage
            return "Error: " & errorMessage
        end try
        '''
        
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            return "WhatsApp Desktop opened. Recent contacts are visible in the sidebar."
        else:
            return "Could not access WhatsApp contacts. Please open WhatsApp manually."
            
    except Exception as e:
        logging.error(f"Error getting WhatsApp contacts: {e}")
        return f"Error getting WhatsApp contacts: {str(e)}"

@function_tool()
async def read_screen_text(
    context: RunContext,  # type: ignore,
    region: str = "full"
) -> str:
    """
    Read and extract all text from the current screen using OCR (Optical Character Recognition).
    Can analyze the entire screen or specific regions.
    
    Args:
        region: Screen region to read ("full", "top", "bottom", "left", "right", "center")
    """
    if not is_mac():
        return "Screen reading is only available on macOS."
    
    try:
        # Check if OCR dependencies are available
        try:
            from PIL import ImageGrab
            import pytesseract
            import numpy as np
        except ImportError:
            return "OCR dependencies not available. Please install: pip install Pillow pytesseract opencv-python"
        
        # Take screenshot
        screenshot = ImageGrab.grab()
        
        # Process different regions
        if region == "top":
            height = screenshot.height
            screenshot = screenshot.crop((0, 0, screenshot.width, height//3))
        elif region == "bottom":
            height = screenshot.height
            screenshot = screenshot.crop((0, 2*height//3, screenshot.width, height))
        elif region == "left":
            width = screenshot.width
            screenshot = screenshot.crop((0, 0, width//2, screenshot.height))
        elif region == "right":
            width = screenshot.width
            screenshot = screenshot.crop((width//2, 0, width, screenshot.height))
        elif region == "center":
            width, height = screenshot.width, screenshot.height
            screenshot = screenshot.crop((width//4, height//4, 3*width//4, 3*height//4))
        
        # Convert to numpy array for better OCR
        img_array = np.array(screenshot)
        
        # Use pytesseract to extract text
        text = pytesseract.image_to_string(img_array, lang='eng+hin')  # English + Hindi support
        
        if text.strip():
            return f"Screen text (region: {region}):\n{text.strip()}"
        else:
            return f"No readable text found in {region} region of screen"
            
    except Exception as e:
        return f"Error reading screen text: {str(e)}"

@function_tool()
async def analyze_screen_content(
    context: RunContext,  # type: ignore,
    analysis_type: str = "general"
) -> str:
    """
    Analyze current screen content and provide detailed information about what's visible.
    
    Args:
        analysis_type: Type of analysis ("general", "ui_elements", "text_fields", "buttons", "applications")
    """
    if not is_mac():
        return "Screen analysis is only available on macOS."
    
    try:
        # Get current screen info
        from .screen_monitoring import get_screen_info
        screen_info = await get_screen_info(context)
        
        # Read screen text
        screen_text = await read_screen_text(context)
        
        # Get running applications
        from .screen_monitoring import get_open_windows_info
        windows_info = await get_open_windows_info(context)
        
        if analysis_type == "general":
            analysis = f"""
SCREEN ANALYSIS - GENERAL OVERVIEW:

{screen_info}

VISIBLE TEXT ON SCREEN:
{screen_text}

RUNNING APPLICATIONS:
{windows_info}
"""
        
        elif analysis_type == "ui_elements":
            # Find UI elements using AppleScript
            script = '''
            tell application "System Events"
                set frontApp to name of first application process whose frontmost is true
                try
                    tell process frontApp
                        set uiElements to every UI element of window 1
                        set elementInfo to ""
                        repeat with element in uiElements
                            try
                                set elementType to class of element as string
                                set elementName to name of element as string
                                set elementInfo to elementInfo & elementType & ": " & elementName & "\n"
                            end try
                        end repeat
                        return elementInfo
                    end tell
                on error
                    return "Could not access UI elements"
                end try
            end tell
            '''
            result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
            ui_elements = result.stdout.strip() if result.returncode == 0 else "UI elements not accessible"
            
            analysis = f"""
SCREEN ANALYSIS - UI ELEMENTS:

ACTIVE APPLICATION UI ELEMENTS:
{ui_elements}

SCREEN TEXT:
{screen_text}
"""
        
        elif analysis_type == "text_fields":
            # Find text fields and input areas
            script = '''
            tell application "System Events"
                set frontApp to name of first application process whose frontmost is true
                try
                    tell process frontApp
                        set textFields to every text field of window 1
                        set textAreas to every text area of window 1
                        set fieldInfo to "TEXT FIELDS:\n"
                        repeat with field in textFields
                            try
                                set fieldValue to value of field as string
                                set fieldName to name of field as string
                                set fieldInfo to fieldInfo & "Field: " & fieldName & " | Value: " & fieldValue & "\n"
                            end try
                        end repeat
                        set fieldInfo to fieldInfo & "\nTEXT AREAS:\n"
                        repeat with area in textAreas
                            try
                                set areaValue to value of area as string
                                set areaName to name of area as string
                                set fieldInfo to fieldInfo & "Area: " & areaName & " | Value: " & areaValue & "\n"
                            end try
                        end repeat
                        return fieldInfo
                    end tell
                on error
                    return "Could not access text fields"
                end try
            end tell
            '''
            result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
            text_fields = result.stdout.strip() if result.returncode == 0 else "Text fields not accessible"
            
            analysis = f"""
SCREEN ANALYSIS - TEXT FIELDS:

{text_fields}

SCREEN TEXT:
{screen_text}
"""
        
        else:
            analysis = f"""
SCREEN ANALYSIS:

{screen_info}
{screen_text}
{windows_info}
"""
        
        return analysis
        
    except Exception as e:
        return f"Error analyzing screen content: {str(e)}"

@function_tool()
async def fill_input_field(
    context: RunContext,  # type: ignore,
    text_to_fill: str,
    field_identifier: str = "active",
    method: str = "type"
) -> str:
    """
    Fill any input field on screen with specified text.
    
    Args:
        text_to_fill: The text to enter in the input field
        field_identifier: How to identify the field ("active", "name:fieldname", "index:1")
        method: How to fill ("type", "paste", "replace")
    """
    if not is_mac():
        return "Input field filling is only available on macOS."
    
    try:
        if field_identifier == "active":
            # Fill the currently active/focused input field
            if method == "paste":
                # Copy text to clipboard and paste
                import pyperclip
                pyperclip.copy(text_to_fill)
                subprocess.run(["osascript", "-e", 'tell application "System Events" to keystroke "v" using command down'], check=True)
                return f"Successfully pasted '{text_to_fill}' into active input field"
            
            elif method == "replace":
                # Select all and replace
                subprocess.run(["osascript", "-e", 'tell application "System Events" to keystroke "a" using command down'], check=True)
                import time
                time.sleep(0.2)
                import pyperclip
                pyperclip.copy(text_to_fill)
                subprocess.run(["osascript", "-e", 'tell application "System Events" to keystroke "v" using command down'], check=True)
                return f"Successfully replaced text with '{text_to_fill}' in active input field"
            
            else:  # type method
                # Type the text directly
                script = f'''
                tell application "System Events"
                    keystroke "{text_to_fill}"
                end tell
                '''
                subprocess.run(["osascript", "-e", script], check=True)
                return f"Successfully typed '{text_to_fill}' into active input field"
        
        elif field_identifier.startswith("name:"):
            # Find field by name
            field_name = field_identifier[5:]
            script = f'''
            tell application "System Events"
                set frontApp to name of first application process whose frontmost is true
                try
                    tell process frontApp
                        set targetField to first text field whose name is "{field_name}"
                        set focused of targetField to true
                        set value of targetField to "{text_to_fill}"
                        return "success"
                    end tell
                on error
                    try
                        tell process frontApp
                            set targetArea to first text area whose name is "{field_name}"
                            set focused of targetArea to true
                            set value of targetArea to "{text_to_fill}"
                            return "success"
                        end tell
                    on error
                        return "field not found"
                    end try
                end try
            end tell
            '''
            result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
            if "success" in result.stdout:
                return f"Successfully filled field '{field_name}' with '{text_to_fill}'"
            else:
                return f"Could not find field named '{field_name}'"
        
        else:
            return "Invalid field identifier. Use 'active', 'name:fieldname', or 'index:number'"
            
    except Exception as e:
        return f"Error filling input field: {str(e)}"

@function_tool()
async def get_active_application_info(
    context: RunContext,  # type: ignore,
) -> str:
    """
    Get detailed information about the currently active application.
    """
    if not is_mac():
        return "This function is only available on macOS."
    
    try:
        # Get active application
        script = '''
        tell application "System Events"
            set frontApp to name of first application process whose frontmost is true
            return frontApp
        end tell
        '''
        
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        active_app = result.stdout.strip() if result.returncode == 0 else "Unknown"
        
        # Get window information for active app
        window_script = f'''
        tell application "System Events"
            tell process "{active_app}"
                set windowList to every window
                set windowInfo to ""
                repeat with win in windowList
                    try
                        set winTitle to title of win
                        set winInfo to "Window: " & winTitle & "\n"
                        set windowInfo to windowInfo & winInfo
                    end try
                end repeat
                return windowInfo
            end tell
        end tell
        '''
        
        window_result = subprocess.run(["osascript", "-e", window_script], capture_output=True, text=True)
        window_info = window_result.stdout.strip() if window_result.returncode == 0 else "Could not get window info"
        
        # Get text content from active app
        text_script = f'''
        tell application "System Events"
            tell process "{active_app}"
                set textElements to every text field of window 1
                set textInfo to ""
                repeat with element in textElements
                    try
                        set elementValue to value of element as string
                        set elementName to name of element as string
                        set textInfo to textInfo & "Field: " & elementName & " | Value: " & elementValue & "\n"
                    end try
                end repeat
                return textInfo
            end tell
        end tell
        '''
        
        text_result = subprocess.run(["osascript", "-e", text_script], capture_output=True, text=True)
        text_info = text_result.stdout.strip() if text_result.returncode == 0 else "Could not get text info"
        
        analysis = f"""
ACTIVE APPLICATION ANALYSIS:

Application: {active_app}

WINDOW INFORMATION:
{window_info}

TEXT FIELDS AND CONTENT:
{text_info}
"""
        
        return analysis
        
    except Exception as e:
        return f"Error getting active application info: {str(e)}"

def get_all_tools() -> List:
    """
    Return all available tools for the agent
    """
    return [
        # Internet and Information Tools
        search_internet,
        get_current_news,
        get_weather_info,
        
        # AI API Tools
        ask_cloud_api_with_internet,
        ask_deepseek_with_internet,
        
        # Mac System Control
        execute_mac_command,
        set_brightness,
        set_volume,
        take_screenshot,
        lock_screen,
        empty_trash,
        
        # Application Control
        open_app,
        close_application,
        control_music,
        
        # File Management
        create_file,
        delete_file,
        read_file_content,
        write_file_content,
        create_folder,
        list_folder_contents,
        copy_file_or_folder,
        move_file_or_folder,
        
        # Communication Tools
        send_email,
        send_whatsapp_message,
        make_phone_call,
        
        # System Information
        get_system_info,
        check_mac_permissions,
        get_downloads_info,
        
        # Screen Monitoring
        get_screen_info,
        get_open_windows_info,
        get_browser_tabs_detailed,
        
        # Advanced Mac Control
        toggle_wifi,
        toggle_bluetooth,
        toggle_dark_mode,
        set_audio_output,
        start_screen_saver,
        set_keyboard_backlight,
        
        # Web Browser Tools
        open_website,
        search_in_browser,
        open_web_search,
        control_browser_music,
        
        # Calendar and Reminders
        get_calendar_events,
        create_reminder,
        
        # Smart Home
        control_smart_home,
        
        # File Search
        find_and_replace_in_file,
        search_in_files,
        
        # Language Tools
        detect_language,
        
        # Advanced System Tools
        set_volume_precise,
        set_brightness_precise,
        open_folder_in_app,
        change_wallpaper,
        
        # Complex AI Tools
        enhanced_internet_query,
        multi_source_analysis,
        
        # WhatsApp Desktop Tools
        send_whatsapp_desktop_message,
        get_whatsapp_contacts,
        
        # Screen Reading Tools
        read_screen_text,
        analyze_screen_content,
        fill_input_field,
        get_active_application_info,
        
        # Screen Monitoring Tools
        read_screen_content,
        read_browser_tab_content,
        monitor_active_application,
        find_text_on_screen,
    ]

def get_tools_description() -> str:
    """
    Return description of all available tools
    """
    return """
    🌐 Internet & Information Tools:
    - search_internet: Search for current information on any topic
    - get_current_news: Get latest news on any topic
    - get_weather_info: Get weather information for any location
    
    🤖 AI & Analysis Tools:
    - ask_cloud_api_with_internet: Ask complex questions with internet context using Claude
    - ask_deepseek_with_internet: Ask complex questions with internet context using DeepSeek
    - enhanced_internet_query: Enhanced internet query with multiple sources
    - multi_source_analysis: Get analysis from multiple sources
    
     Mac System Control:
    - execute_mac_command: Execute various Mac system commands
    - set_brightness: Set screen brightness (0-100)
    - set_volume: Set system volume (0-100)
    - take_screenshot: Take screenshot
    - lock_screen: Lock the Mac screen
    - empty_trash: Empty the trash
    
    📱 Application Control:
    - open_app: Open any application
    - close_application: Close any application
    - control_music: Control music playback (play, pause, next, etc.)
    
    📁 File Management:
    - create_file: Create new files
    - delete_file: Delete files (move to trash)
    - read_file_content: Read file content
    - write_file_content: Write content to files
    - create_folder: Create new folders
    - list_folder_contents: List folder contents
    - copy_file_or_folder: Copy files/folders
    - move_file_or_folder: Move files/folders
    
    📧 Communication Tools:
    - send_email: Send emails via Gmail
    - send_whatsapp_message: Send WhatsApp messages
    - make_phone_call: Make phone calls
    
     System Information:
    - get_system_info: Get system information (battery, storage, etc.)
    - check_mac_permissions: Check Mac permissions
    - get_downloads_info: Get Downloads folder analysis
    
    ️ Screen Monitoring:
    - get_screen_info: Get information about what's on screen
    - get_open_windows_info: Get detailed window information
    - get_browser_tabs_detailed: Get browser tabs information
    
    ⚙️ Advanced Mac Control:
    - toggle_wifi: Toggle WiFi on/off
    - toggle_bluetooth: Toggle Bluetooth on/off
    - toggle_dark_mode: Toggle dark mode
    - set_audio_output: Set audio output device
    - start_screen_saver: Start screen saver
    - set_keyboard_backlight: Set keyboard backlight
    
    🌐 Web & Browser Tools:
    - open_website: Open popular websites
    - search_in_browser: Search in browser
    - open_web_search: Open web search
    - control_browser_music: Control music in browser
    
    📅 Calendar & Reminders:
    - get_calendar_events: Get calendar events
    - create_reminder: Create reminders
    
    🏠 Smart Home:
    - control_smart_home: Control smart home devices
    
     File Search:
    - find_and_replace_in_file: Find and replace text in files
    - search_in_files: Search for text in files
    
    🌍 Language Tools:
    - detect_language: Detect if text is Hindi or English
    
    🎛️ Advanced System Tools:
    - set_volume_precise: Set volume with precise control
    - set_brightness_precise: Set brightness with precise control
    - open_folder_in_app: Open folders in specific applications
    - change_wallpaper: Change Mac wallpaper
    
    📱 WhatsApp Desktop Tools:
    - send_whatsapp_desktop_message: Send messages using WhatsApp Desktop app
    - get_whatsapp_contacts: Get list of recent WhatsApp contacts
    
    📖 Screen Reading Tools:
    - read_screen_text: Read text from screen using OCR
    - analyze_screen_content: Analyze what's visible on screen
    - fill_input_field: Fill input fields with text
    - get_active_application_info: Get info about active application
    """ 