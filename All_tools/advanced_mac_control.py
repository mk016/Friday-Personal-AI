import logging
import subprocess
import os
import smtplib
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText
from typing import Optional
from livekit.agents import function_tool, RunContext
import platform

def is_mac():
    """Check if running on Mac"""
    return platform.system() == "Darwin"

@function_tool()
async def toggle_wifi(
    context: RunContext,  # type: ignore
) -> str:
    """
    Toggle WiFi on/off on Mac.
    """
    if not is_mac():
        return "This function is only supported on macOS."
    try:
        # Get current WiFi status
        result = subprocess.run(["networksetup", "-getairportpower", "en0"], capture_output=True, text=True)
        current_status = "On" in result.stdout
        
        # Toggle WiFi
        new_status = "Off" if current_status else "On"
        subprocess.run(["networksetup", "-setairportpower", "en0", new_status], check=True)
        return f"WiFi turned {new_status}"
    except Exception as e:
        logging.error(f"Error toggling WiFi: {e}")
        return f"Failed to toggle WiFi: {e}"

@function_tool()
async def toggle_bluetooth(
    context: RunContext,  # type: ignore
) -> str:
    """
    Toggle Bluetooth on/off on Mac.
    """
    if not is_mac():
        return "This function is only supported on macOS."
    try:
        script = '''
        tell application "System Preferences"
            reveal pane "com.apple.preferences.Bluetooth"
        end tell
        tell application "System Events"
            tell process "System Preferences"
                click button "Turn Bluetooth On" of window 1
            end tell
        end tell
        '''
        subprocess.run(["osascript", "-e", script], check=True)
        return "Bluetooth toggled"
    except Exception as e:
        logging.error(f"Error toggling Bluetooth: {e}")
        return f"Failed to toggle Bluetooth: {e}"

@function_tool()
async def toggle_dark_mode(
    context: RunContext,  # type: ignore
) -> str:
    """
    Toggle dark mode on Mac.
    """
    if not is_mac():
        return "This function is only supported on macOS."
    try:
        script = '''
        tell application "System Events"
            tell appearance preferences
                set dark mode to not dark mode
            end tell
        end tell
        '''
        subprocess.run(["osascript", "-e", script], check=True)
        return "Dark mode toggled"
    except Exception as e:
        logging.error(f"Error toggling dark mode: {e}")
        return f"Failed to toggle dark mode: {e}"

@function_tool()
async def set_audio_output(
    context: RunContext,  # type: ignore
    device: str
) -> str:
    """
    Set audio output device on Mac.
    """
    if not is_mac():
        return "This function is only supported on macOS."
    try:
        script = f'''
        tell application "System Preferences"
            reveal anchor "output" of pane "com.apple.preference.sound"
        end tell
        tell application "System Events"
            tell process "System Preferences"
                select (row 1 of table 1 of scroll area 1 of tab group 1 of window 1 where value of text field 1 is "{device}")
            end tell
        end tell
        '''
        subprocess.run(["osascript", "-e", script], check=True)
        return f"Audio output set to {device}"
    except Exception as e:
        logging.error(f"Error setting audio output: {e}")
        return f"Failed to set audio output: {e}"

@function_tool()
async def start_screen_saver(
    context: RunContext,  # type: ignore
) -> str:
    """
    Start screen saver on Mac.
    """
    if not is_mac():
        return "This function is only supported on macOS."
    try:
        script = '''
        tell application "System Events"
            start current screen saver
        end tell
        '''
        subprocess.run(["osascript", "-e", script], check=True)
        return "Screen saver started"
    except Exception as e:
        logging.error(f"Error starting screen saver: {e}")
        return f"Failed to start screen saver: {e}"

@function_tool()
async def set_keyboard_backlight(
    context: RunContext,  # type: ignore
    level: int
) -> str:
    """
    Set keyboard backlight level (0-100) on Mac.
    """
    if not is_mac():
        return "This function is only supported on macOS."
    try:
        if not 0 <= level <= 100:
            return "Keyboard backlight level must be between 0 and 100."
        
        script = f'''
        tell application "System Events"
            tell process "TouchBarServer"
                set value of first slider of group 1 of window 1 to {level}
            end tell
        end tell
        '''
        subprocess.run(["osascript", "-e", script], check=True)
        return f"Keyboard backlight set to {level}%"
    except Exception as e:
        logging.error(f"Error setting keyboard backlight: {e}")
        return f"Failed to set keyboard backlight: {e}"

@function_tool()
async def send_email(
    context: RunContext,  # type: ignore
    to_email: str,
    subject: str,
    message: str,
    cc_email: Optional[str] = None
) -> str:
    """
    Send an email through Gmail.
    
    Args:
        to_email: Recipient email address
        subject: Email subject line
        message: Email body content
        cc_email: Optional CC email address
    """
    try:
        # Gmail SMTP configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        # Get credentials from environment variables
        gmail_user = os.getenv("GMAIL_USER")
        gmail_password = os.getenv("GMAIL_APP_PASSWORD")  # Use App Password, not regular password
        
        if not gmail_user or not gmail_password:
            logging.error("Gmail credentials not found in environment variables")
            return "Email sending failed: Gmail credentials not configured."
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add CC if provided
        recipients = [to_email]
        if cc_email:
            msg['Cc'] = cc_email
            recipients.append(cc_email)
        
        # Attach message body
        msg.attach(MIMEText(message, 'plain'))
        
        # Connect to Gmail SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS encryption
        server.login(gmail_user, gmail_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(gmail_user, recipients, text)
        server.quit()
        
        logging.info(f"Email sent successfully to {to_email}")
        return f"Email sent successfully to {to_email}"
        
    except smtplib.SMTPAuthenticationError:
        logging.error("Gmail authentication failed")
        return "Email sending failed: Authentication error. Please check your Gmail credentials."
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error occurred: {e}")
        return f"Email sending failed: SMTP error - {str(e)}"
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return f"An error occurred while sending email: {str(e)}"

@function_tool()
async def send_whatsapp_message(
    context: RunContext,  # type: ignore
    contact_name: str,
    message: str
) -> str:
    """
    Send WhatsApp message to a contact using Mac automation.
    Args:
        contact_name: Name of the contact to send message to
        message: Message content to send
    """
    try:
        logging.info(f"Sending WhatsApp message to {contact_name}: {message}")
        
        if not is_mac():
            return "यह फीचर केवल Mac पर उपलब्ध है। / This feature is only available on Mac."
        
        # Improved AppleScript for WhatsApp Web
        applescript = f'''
        try
            -- Open WhatsApp Web if not already open
            tell application "Safari"
                activate
                delay 0.5
                
                -- Check if WhatsApp Web is already open
                set whatsappFound to false
                repeat with thisTab in every tab of front window
                    if URL of thisTab contains "web.whatsapp.com" then
                        set current tab of front window to thisTab
                        set whatsappFound to true
                        exit repeat
                    end if
                end repeat
                
                -- If not found, open new tab with WhatsApp Web
                if not whatsappFound then
                    tell front window
                        set current tab to (make new tab with properties {{URL:"https://web.whatsapp.com"}})
                    end tell
                    delay 3
                end if
            end tell
            
            delay 1
            
            -- Use WhatsApp Web interface
            tell application "System Events"
                tell process "Safari"
                    -- Search for contact
                    keystroke "f" using {{command down}}
                    delay 0.5
                    keystroke "{contact_name}"
                    delay 1.5
                    key code 36  -- Enter key
                    delay 1
                    
                    -- Type message in message box
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
                              capture_output=True, text=True, timeout=45)
        
        if result.returncode == 0 and "successfully" in result.stdout:
            logging.info(f"WhatsApp message sent successfully to {contact_name}")
            return f"✅ WhatsApp message sent to {contact_name}: '{message}'"
        else:
            # Fallback - just open WhatsApp Web
            subprocess.run(['open', 'https://web.whatsapp.com'], timeout=10)
            return f"📱 WhatsApp Web खोला गया। Please manually send message to {contact_name}: '{message}'"
            
    except Exception as e:
        logging.error(f"Error sending WhatsApp message: {e}")
        return f"WhatsApp message भेजने में error: {str(e)}. Manual भेजना होगा।"

@function_tool()
async def make_phone_call(
    context: RunContext,  # type: ignore
    contact_name: str
) -> str:
    """
    Make phone call using Mac (if iPhone nearby with Handoff enabled).
    Args:
        contact_name: Name of contact to call
    """
    try:
        logging.info(f"Making phone call to: {contact_name}")
        
        if not is_mac():
            return "यह फीचर केवल Mac पर उपलब्ध है। / This feature is only available on Mac."
        
        # Try to use FaceTime or Contacts app for calling
        applescript = f'''
        try
            tell application "FaceTime"
                activate
                delay 1
            end tell
            
            tell application "System Events"
                tell process "FaceTime"
                    keystroke "{contact_name}"
                    delay 1
                    key code 36  -- Enter
                end tell
            end tell
        on error
            tell application "Contacts"
                activate
                delay 1
            end tell
            return "Contacts app खोला गया - manually call करें"
        end try
        '''
        
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=20)
        
        if result.returncode == 0:
            return f"📞 Calling {contact_name} via FaceTime/Phone"
        else:
            return f"📱 {contact_name} को call करने के लिए FaceTime/Contacts app खोला गया"
            
    except Exception as e:
        logging.error(f"Error making phone call: {e}")
        return f"Phone call में error: {str(e)}"