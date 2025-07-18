import logging
import subprocess
import os
import platform
from livekit.agents import function_tool, RunContext

def is_mac():
    """Check if running on Mac"""
    return platform.system() == "Darwin"

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