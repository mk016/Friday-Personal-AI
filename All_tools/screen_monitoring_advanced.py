import logging
import pyautogui
import cv2
import numpy as np
from PIL import Image
import pytesseract
import subprocess
import os
import platform
from livekit.agents import function_tool, RunContext
import time

def is_mac():
    """Check if running on Mac"""
    return platform.system() == "Darwin"

@function_tool()
async def read_screen_content(
    context: RunContext,  # type: ignore
    area: str = "full_screen"
) -> str:
    """
    Read and extract text content from the current screen.
    Args:
        area: Area to read - "full_screen", "browser", "active_window", or "specific" (x,y,width,height)
    """
    try:
        logging.info(f"Reading screen content from area: {area}")
        
        # Take screenshot
        screenshot = pyautogui.screenshot()
        
        if area == "full_screen":
            # Read full screen
            text = pytesseract.image_to_string(screenshot)
        elif area == "browser":
            # Focus on browser area (top 70% of screen)
            browser_area = screenshot.crop((0, 0, screenshot.width, int(screenshot.height * 0.7)))
            text = pytesseract.image_to_string(browser_area)
        elif area == "active_window":
            # Try to get active window
            try:
                # On Mac, get active window bounds
                if is_mac():
                    result = subprocess.run(['osascript', '-e', 'tell application "System Events" to get position and size of window 1 of (process 1 where it is frontmost)'], 
                                         capture_output=True, text=True)
                    if result.returncode == 0:
                        # Parse window bounds and crop screenshot
                        bounds = result.stdout.strip().split(', ')
                        x, y, width, height = map(int, bounds)
                        window_area = screenshot.crop((x, y, x + width, y + height))
                        text = pytesseract.image_to_string(window_area)
                    else:
                        text = pytesseract.image_to_string(screenshot)
                else:
                    text = pytesseract.image_to_string(screenshot)
            except:
                text = pytesseract.image_to_string(screenshot)
        else:
            text = pytesseract.image_to_string(screenshot)
        
        # Clean up text
        if text.strip():
            cleaned_text = text.strip()
            return f"📱 Screen Content ({area}):\n\n{cleaned_text}"
        else:
            return "No readable text found on screen."
            
    except Exception as e:
        logging.error(f"Error reading screen: {e}")
        return f"Error reading screen content: {str(e)}"

@function_tool()
async def read_browser_tab_content(
    context: RunContext,  # type: ignore
    browser_name: str = "chrome"
) -> str:
    """
    Read content from the active browser tab.
    Args:
        browser_name: Browser name (chrome, safari, firefox)
    """
    try:
        logging.info(f"Reading browser tab content from: {browser_name}")
        
        # Activate browser first
        if is_mac():
            subprocess.run(['osascript', '-e', f'tell application "{browser_name}" to activate'])
            time.sleep(1)  # Wait for browser to activate
        
        # Take screenshot of browser area
        screenshot = pyautogui.screenshot()
        
        # Focus on browser content area (avoid address bar and bookmarks)
        # Adjust these values based on your browser layout
        browser_content = screenshot.crop((
            50,  # Left margin
            100,  # Top margin (avoid address bar)
            screenshot.width - 50,  # Right margin
            screenshot.height - 100  # Bottom margin
        ))
        
        # Extract text
        text = pytesseract.image_to_string(browser_content)
        
        if text.strip():
            # Get current URL if possible
            try:
                if is_mac():
                    url_result = subprocess.run([
                        'osascript', '-e', 
                        f'tell application "{browser_name}" to get URL of active tab of front window'
                    ], capture_output=True, text=True)
                    current_url = url_result.stdout.strip() if url_result.returncode == 0 else "Unknown URL"
                else:
                    current_url = "Unknown URL"
            except:
                current_url = "Unknown URL"
            
            cleaned_text = text.strip()
            return f"🌐 Browser Tab Content ({browser_name}):\n\nURL: {current_url}\n\nContent:\n{cleaned_text}"
        else:
            return f"No readable content found in {browser_name} tab."
            
    except Exception as e:
        logging.error(f"Error reading browser tab: {e}")
        return f"Error reading browser tab content: {str(e)}"

@function_tool()
async def monitor_active_application(
    context: RunContext,  # type: ignore
) -> str:
    """
    Monitor what application is currently active and what's happening on screen.
    """
    try:
        logging.info("Monitoring active application")
        
        # Get active application
        if is_mac():
            app_result = subprocess.run([
                'osascript', '-e', 
                'tell application "System Events" to get name of first process where it is frontmost'
            ], capture_output=True, text=True)
            active_app = app_result.stdout.strip() if app_result.returncode == 0 else "Unknown"
        else:
            active_app = "Unknown"
        
        # Take screenshot
        screenshot = pyautogui.screenshot()
        
        # Extract text from screen
        text = pytesseract.image_to_string(screenshot)
        
        # Get window title if possible
        try:
            if is_mac():
                title_result = subprocess.run([
                    'osascript', '-e',
                    'tell application "System Events" to get name of window 1 of (process 1 where it is frontmost)'
                ], capture_output=True, text=True)
                window_title = title_result.stdout.strip() if title_result.returncode == 0 else "Unknown"
            else:
                window_title = "Unknown"
        except:
            window_title = "Unknown"
        
        result = f"�� Active Application Monitor:\n\n"
        result += f"Active App: {active_app}\n"
        result += f"Window Title: {window_title}\n\n"
        
        if text.strip():
            result += f"Screen Content:\n{text.strip()}"
        else:
            result += "No readable text found on screen."
        
        return result
        
    except Exception as e:
        logging.error(f"Error monitoring application: {e}")
        return f"Error monitoring active application: {str(e)}"

@function_tool()
async def find_text_on_screen(
    context: RunContext,  # type: ignore
    search_text: str
) -> str:
    """
    Search for specific text on the current screen.
    Args:
        search_text: Text to search for on screen
    """
    try:
        logging.info(f"Searching for text on screen: {search_text}")
        
        # Take screenshot
        screenshot = pyautogui.screenshot()
        
        # Extract all text from screen
        all_text = pytesseract.image_to_string(screenshot)
        
        # Search for the text
        if search_text.lower() in all_text.lower():
            # Find the context around the text
            lines = all_text.split('\n')
            found_lines = []
            
            for line in lines:
                if search_text.lower() in line.lower():
                    found_lines.append(line.strip())
            
            if found_lines:
                result = f"✅ Found '{search_text}' on screen:\n\n"
                for line in found_lines:
                    result += f"• {line}\n"
                return result
            else:
                return f"Text '{search_text}' found but couldn't extract context."
        else:
            return f"❌ Text '{search_text}' not found on screen."
            
    except Exception as e:
        logging.error(f"Error searching text on screen: {e}")
        return f"Error searching text on screen: {str(e)}" 