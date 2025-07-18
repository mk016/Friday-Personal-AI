import logging
import subprocess
import os
import platform
from livekit.agents import function_tool, RunContext

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