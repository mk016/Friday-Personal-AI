import logging
import subprocess
import os
import platform
import urllib.parse
from livekit.agents import function_tool, RunContext

def is_mac():
    """Check if running on Mac"""
    return platform.system() == "Darwin"

@function_tool()
async def open_website(
    context: RunContext,  # type: ignore
    website_name: str
) -> str:
    """
    Open popular websites quickly (YouTube, Instagram, Facebook, Twitter, etc.).
    Args:
        website_name: Name of website to open (youtube, instagram, facebook, twitter, etc.)
    """
    try:
        logging.info(f"Opening website: {website_name}")
        
        if not is_mac():
            return "यह फीचर केवल Mac पर उपलब्ध है। / This feature is only available on Mac."
        
        websites = {
            "youtube": "https://youtube.com",
            "instagram": "https://instagram.com", 
            "facebook": "https://facebook.com",
            "twitter": "https://twitter.com",
            "whatsapp": "https://web.whatsapp.com",
            "gmail": "https://gmail.com",
            "google": "https://google.com",
            "github": "https://github.com",
            "linkedin": "https://linkedin.com",
            "netflix": "https://netflix.com",
            "amazon": "https://amazon.in",
            "flipkart": "https://flipkart.com",
            "spotify": "https://open.spotify.com",
            "reddit": "https://reddit.com"
        }
        
        url = websites.get(website_name.lower())
        if not url:
            url = f"https://{website_name}.com"
        
        applescript = f'''
        tell application "Safari"
            activate
            open location "{url}"
        end tell
        '''
        
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            logging.info(f"Website opened successfully: {website_name}")
            return f"🌐 {website_name.title()} website खोल दी। / Opened {website_name.title()} website."
        else:
            return f"❌ Website खोलने में समस्या: {result.stderr}"
            
    except Exception as e:
        logging.error(f"Error opening website: {e}")
        return f"Website खोलने में error: {str(e)}"

@function_tool()
async def search_in_browser(
    context: RunContext,  # type: ignore
    query: str,
    browser: str = "safari"
) -> str:
    """
    Search something in browser (Safari, Chrome, Firefox).
    Args:
        query: What to search for
        browser: Browser to use (safari, chrome, firefox)
    """
    try:
        logging.info(f"Searching '{query}' in {browser}")
        
        if not is_mac():
            return "यह फीचर केवल Mac पर उपलब्ध है। / This feature is only available on Mac."
        
        # Format search URL
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        
        browser_apps = {
            "safari": "Safari",
            "chrome": "Google Chrome", 
            "firefox": "Firefox"
        }
        
        app_name = browser_apps.get(browser.lower(), "Safari")
        
        # AppleScript to open browser and search
        applescript = f'''
        tell application "{app_name}"
            activate
            delay 1
            open location "{search_url}"
        end tell
        '''
        
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            logging.info(f"Browser search opened successfully: {query}")
            return f"🔍 {app_name} में '{query}' search कर दिया। / Opened search for '{query}' in {app_name}."
        else:
            return f"❌ Browser search में समस्या: {result.stderr}"
            
    except Exception as e:
        logging.error(f"Error with browser search: {e}")
        return f"Browser search में error: {str(e)}"

@function_tool()
async def open_web_search(
    context: RunContext,  # type: ignore
    query: str,
    site: str = ""
) -> str:
    """
    Open web search in browser with specific query.
    Args:
        query: Search query
        site: Specific site to search (youtube, google, wikipedia, etc.)
    """
    try:
        encoded_query = urllib.parse.quote(query)
        
        site = site.lower()
        
        if site in ["youtube", "yt"]:
            url = f"https://www.youtube.com/results?search_query={encoded_query}"
        elif site in ["google", ""]:
            url = f"https://www.google.com/search?q={encoded_query}"
        elif site in ["wikipedia", "wiki"]:
            url = f"https://en.wikipedia.org/wiki/Special:Search?search={encoded_query}"
        elif site in ["github"]:
            url = f"https://github.com/search?q={encoded_query}"
        elif site in ["stackoverflow", "stack"]:
            url = f"https://stackoverflow.com/search?q={encoded_query}"
        elif site in ["reddit"]:
            url = f"https://www.reddit.com/search/?q={encoded_query}"
        elif site in ["twitter", "x"]:
            url = f"https://twitter.com/search?q={encoded_query}"
        elif site in ["amazon"]:
            url = f"https://www.amazon.com/s?k={encoded_query}"
        else:
            url = f"https://www.google.com/search?q={encoded_query}"
            
        subprocess.run(["open", url], check=True)
        
        if site:
            return f"✅ Opened {site.title()} search for: {query}"
        else:
            return f"✅ Opened Google search for: {query}"
        
    except Exception as e:
        logging.error(f"Error opening web search: {e}")
        return f"❌ Web search open करने में error: {str(e)}"

@function_tool()
async def control_browser_music(
    context: RunContext,  # type: ignore
    action: str,
    platform: str = "youtube"
) -> str:
    """
    Control music playback in browser (YouTube, Spotify Web, etc.).
    Args:
        action: play, pause, next, previous, stop
        platform: youtube, spotify, apple_music, etc.
    """
    if not is_mac():
        return "Browser music control केवल macOS पर उपलब्ध है।"
    
    try:
        action = action.lower()
        platform = platform.lower()
        
        # JavaScript commands for different platforms
        if platform in ["youtube", "yt"]:
            if action == "play":
                js_command = "document.querySelector('video').play()"
            elif action == "pause":
                js_command = "document.querySelector('video').pause()"
            elif action == "next":
                js_command = "document.querySelector('button[aria-label*=\"Next\"]').click()"
            elif action == "previous":
                js_command = "document.querySelector('button[aria-label*=\"Previous\"]').click()"
            elif action == "stop":
                js_command = "document.querySelector('video').pause(); document.querySelector('video').currentTime = 0"
            else:
                return f"❌ Unknown action: {action}"
                
        elif platform in ["spotify"]:
            if action == "play":
                js_command = "document.querySelector('[data-testid=\"control-button-playpause\"]').click()"
            elif action == "pause":
                js_command = "document.querySelector('[data-testid=\"control-button-playpause\"]').click()"
            elif action == "next":
                js_command = "document.querySelector('[data-testid=\"control-button-skip-forward\"]').click()"
            elif action == "previous":
                js_command = "document.querySelector('[data-testid=\"control-button-skip-back\"]').click()"
            else:
                return f"❌ Unknown action: {action}"
        else:
            return f"❌ Unsupported platform: {platform}"
            
        # Execute JavaScript in Safari
        safari_script = f'''
        tell application "Safari"
            tell front document
                do JavaScript "{js_command}"
            end tell
        end tell
        '''
        
        # Try Safari first
        try:
            subprocess.run(["osascript", "-e", safari_script], check=True)
            return f"✅ {action.title()} command sent to {platform.title()} in Safari"
        except:
            pass
            
        # Try Chrome
        chrome_script = f'''
        tell application "Google Chrome"
            tell active tab of front window
                execute javascript "{js_command}"
            end tell
        end tell
        '''
        
        try:
            subprocess.run(["osascript", "-e", chrome_script], check=True)
            return f"✅ {action.title()} command sent to {platform.title()} in Chrome"
        except:
            pass
            
        return f"❌ Could not control {platform}. Make sure browser is open with {platform} tab active."
        
    except Exception as e:
        logging.error(f"Error controlling browser music: {e}")
        return f"❌ Browser music control में error: {str(e)}" 