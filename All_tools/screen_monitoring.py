import logging
import subprocess
import os
import platform
from livekit.agents import function_tool, RunContext

def is_mac():
    """Check if running on Mac"""
    return platform.system() == "Darwin"

@function_tool()
async def get_screen_info(
    context: RunContext,  # type: ignore
) -> str:
    """
    Get information about what's currently visible on screen - open applications, windows, tabs etc.
    """
    try:
        logging.info("Getting screen information")
        
        result = "🖥️ Screen Information:\n"
        result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # Get running applications
        app_script = '''
        tell application "System Events"
            set runningApps to name of every application process whose visible is true
            return runningApps
        end tell
        '''
        
        app_result = subprocess.run(['osascript', '-e', app_script], 
                                   capture_output=True, text=True, timeout=10)
        
        if app_result.returncode == 0:
            apps = app_result.stdout.strip().split(', ')
            apps = [app.strip() for app in apps if app.strip()]
            
            result += f"🚀 चल रहे Applications ({len(apps)}):\n"
            for i, app in enumerate(apps, 1):
                result += f"  {i}. {app}\n"
            result += "\n"
        
        # Get Safari tabs if Safari is running
        if any('Safari' in app for app in apps):
            safari_script = '''
            tell application "Safari"
                set tabInfo to ""
                repeat with w from 1 to count of windows
                    repeat with t from 1 to count of tabs of window w
                        set tabInfo to tabInfo & "Window " & w & " Tab " & t & ": " & name of tab t of window w & "\n"
                    end repeat
                end repeat
                return tabInfo
            end tell
            '''
            
            try:
                safari_result = subprocess.run(['osascript', '-e', safari_script], 
                                             capture_output=True, text=True, timeout=10)
                
                if safari_result.returncode == 0 and safari_result.stdout.strip():
                    tabs = safari_result.stdout.strip().split('\n')
                    tabs = [tab.strip() for tab in tabs if tab.strip()]
                    
                    result += f"🌐 Safari Tabs ({len(tabs)}):\n"
                    for tab in tabs[:10]:  # Show max 10 tabs
                        result += f"  📄 {tab}\n"
                    if len(tabs) > 10:
                        result += f"  ... और {len(tabs) - 10} tabs\n"
                    result += "\n"
            except:
                result += "🌐 Safari tabs information उपलब्ध नहीं है\n\n"
        
        # Get Chrome tabs if Chrome is running
        if any('Chrome' in app for app in apps):
            chrome_script = '''
            tell application "Google Chrome"
                set tabInfo to ""
                repeat with w from 1 to count of windows
                    repeat with t from 1 to count of tabs of window w
                        set tabInfo to tabInfo & "Window " & w & " Tab " & t & ": " & title of tab t of window w & "\n"
                    end repeat
                end repeat
                return tabInfo
            end tell
            '''
            
            try:
                chrome_result = subprocess.run(['osascript', '-e', chrome_script], 
                                             capture_output=True, text=True, timeout=10)
                
                if chrome_result.returncode == 0 and chrome_result.stdout.strip():
                    tabs = chrome_result.stdout.strip().split('\n')
                    tabs = [tab.strip() for tab in tabs if tab.strip()]
                    
                    result += f"🌐 Chrome Tabs ({len(tabs)}):\n"
                    for tab in tabs[:10]:  # Show max 10 tabs
                        result += f"  📄 {tab}\n"
                    if len(tabs) > 10:
                        result += f"  ... और {len(tabs) - 10} tabs\n"
                    result += "\n"
            except:
                result += "🌐 Chrome tabs information उपलब्ध नहीं है\n\n"
        
        # Get current window information
        window_script = '''
        tell application "System Events"
            set frontApp to name of first application process whose frontmost is true
            return frontApp
        end tell
        '''
        
        window_result = subprocess.run(['osascript', '-e', window_script], 
                                     capture_output=True, text=True, timeout=10)
        
        if window_result.returncode == 0:
            front_app = window_result.stdout.strip()
            result += f"�� Active Application: {front_app}\n\n"
        
        # Get desktop information
        desktop_script = '''
        tell application "Finder"
            set itemCount to count of items in desktop
            return itemCount
        end tell
        '''
        
        desktop_result = subprocess.run(['osascript', '-e', desktop_script], 
                                      capture_output=True, text=True, timeout=10)
        
        if desktop_result.returncode == 0:
            desktop_items = desktop_result.stdout.strip()
            result += f"��️ Desktop पर items: {desktop_items}\n"
        
        return result
        
    except Exception as e:
        logging.error(f"Error getting screen info: {e}")
        return f"❌ Screen information लेने में error: {str(e)}"

@function_tool()
async def get_open_windows_info(
    context: RunContext,  # type: ignore
) -> str:
    """
    Get detailed information about all open windows and their positions
    """
    try:
        logging.info("Getting open windows information")
        
        # Get all open windows with details
        windows_script = '''
        tell application "System Events"
            set windowInfo to ""
            repeat with proc in application processes
                if visible of proc is true then
                    set appName to name of proc
                    repeat with win in windows of proc
                        try
                            set winTitle to title of win
                            set winSize to size of win
                            set winPos to position of win
                            set windowInfo to windowInfo & appName & " | " & winTitle & " | Size: " & item 1 of winSize & "x" & item 2 of winSize & " | Position: " & item 1 of winPos & "," & item 2 of winPos & "\n"
                        end try
                    end repeat
                end if
            end repeat
            return windowInfo
        end tell
        '''
        
        windows_result = subprocess.run(['osascript', '-e', windows_script], 
                                       capture_output=True, text=True, timeout=15)
        
        if windows_result.returncode == 0 and windows_result.stdout.strip():
            windows = windows_result.stdout.strip().split('\n')
            windows = [win.strip() for win in windows if win.strip()]
            
            result = f"�� Open Windows ({len(windows)}):\n"
            result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            
            for i, window in enumerate(windows, 1):
                parts = window.split(' | ')
                if len(parts) >= 4:
                    app_name = parts[0]
                    win_title = parts[1]
                    size_info = parts[2]
                    pos_info = parts[3]
                    
                    result += f"{i}. 📱 {app_name}\n"
                    result += f"   📄 Title: {win_title}\n"
                    result += f"   �� {size_info} | 📍 {pos_info}\n\n"
                
                if i >= 15:  # Limit to 15 windows for readability
                    result += f"... और {len(windows) - 15} windows\n"
                    break
            
            return result
        else:
            return "❌ Windows information नहीं मिली"
        
    except Exception as e:
        logging.error(f"Error getting windows info: {e}")
        return f"❌ Windows information लेने में error: {str(e)}"

@function_tool()
async def get_browser_tabs_detailed(
    context: RunContext,  # type: ignore
    browser: str = "all"
) -> str:
    """
    Get detailed information about browser tabs
    
    Args:
        browser: Which browser to check ("safari", "chrome", "firefox", or "all")
    """
    try:
        logging.info(f"Getting detailed browser tabs for: {browser}")
        
        result = "🌐 Browser Tabs Information:\n"
        result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # Safari tabs
        if browser in ["safari", "all"]:
            safari_script = '''
            tell application "Safari"
                set tabInfo to ""
                repeat with w from 1 to count of windows
                    repeat with t from 1 to count of tabs of window w
                        set tabName to name of tab t of window w
                        set tabURL to URL of tab t of window w
                        set tabInfo to tabInfo & "W" & w & "T" & t & "|" & tabName & "|" & tabURL & "\n"
                    end repeat
                end repeat
                return tabInfo
            end tell
            '''
            
            try:
                safari_result = subprocess.run(['osascript', '-e', safari_script], 
                                             capture_output=True, text=True, timeout=10)
                
                if safari_result.returncode == 0 and safari_result.stdout.strip():
                    tabs = safari_result.stdout.strip().split('\n')
                    tabs = [tab.strip() for tab in tabs if tab.strip()]
                    
                    result += f"🍎 Safari Tabs ({len(tabs)}):\n"
                    for i, tab in enumerate(tabs[:10], 1):
                        parts = tab.split('|')
                        if len(parts) >= 3:
                            window_tab = parts[0]
                            title = parts[1]
                            url = parts[2]
                            result += f"  {i}. {window_tab}: {title}\n"
                            result += f"     🔗 {url[:50]}{'...' if len(url) > 50 else ''}\n"
                    
                    if len(tabs) > 10:
                        result += f"  ... और {len(tabs) - 10} Safari tabs\n"
                    result += "\n"
                else:
                    result += "�� Safari नहीं चल रहा या tabs नहीं मिलीं\n\n"
            except:
                result += "�� Safari tabs access नहीं हो सका\n\n"
        
        # Chrome tabs
        if browser in ["chrome", "all"]:
            chrome_script = '''
            tell application "Google Chrome"
                set tabInfo to ""
                repeat with w from 1 to count of windows
                    repeat with t from 1 to count of tabs of window w
                        set tabTitle to title of tab t of window w
                        set tabURL to URL of tab t of window w
                        set tabInfo to tabInfo & "W" & w & "T" & t & "|" & tabTitle & "|" & tabURL & "\n"
                    end repeat
                end repeat
                return tabInfo
            end tell
            '''
            
            try:
                chrome_result = subprocess.run(['osascript', '-e', chrome_script], 
                                             capture_output=True, text=True, timeout=10)
                
                if chrome_result.returncode == 0 and chrome_result.stdout.strip():
                    tabs = chrome_result.stdout.strip().split('\n')
                    tabs = [tab.strip() for tab in tabs if tab.strip()]
                    
                    result += f"🌐 Chrome Tabs ({len(tabs)}):\n"
                    for i, tab in enumerate(tabs[:10], 1):
                        parts = tab.split('|')
                        if len(parts) >= 3:
                            window_tab = parts[0]
                            title = parts[1]
                            url = parts[2]
                            result += f"  {i}. {window_tab}: {title}\n"
                            result += f"     🔗 {url[:50]}{'...' if len(url) > 50 else ''}\n"
                    
                    if len(tabs) > 10:
                        result += f"  ... और {len(tabs) - 10} Chrome tabs\n"
                    result += "\n"
                else:
                    result += "�� Chrome नहीं चल रहा या tabs नहीं मिलीं\n\n"
            except:
                result += "�� Chrome tabs access नहीं हो सका\n\n"
        
        return result
        
    except Exception as e:
        logging.error(f"Error getting browser tabs: {e}")
        return f"❌ Browser tabs information लेने में error: {str(e)}" 