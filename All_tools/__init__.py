# Import all tools for easy access
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
from .automation_tools import create_workflow, batch_file_operations, system_health_check, smart_automation

# Import tools manager
from .tools_manager import get_all_tools, get_tools_description

# List all available tools
__all__ = [
    # Internet and Information Tools
    'search_internet',
    'get_current_news', 
    'get_weather_info',
    
    # AI API Tools
    'ask_cloud_api_with_internet',
    'ask_deepseek_with_internet',
    
    # Mac System Control
    'execute_mac_command',
    'set_brightness',
    'set_volume',
    'take_screenshot',
    'lock_screen',
    'empty_trash',
    
    # Application Control
    'open_app',
    'close_application',
    'control_music',
    
    # File Management
    'create_file',
    'delete_file',
    'read_file_content',
    'write_file_content',
    'create_folder',
    'list_folder_contents',
    'copy_file_or_folder',
    'move_file_or_folder',
    
    # Communication Tools
    'send_email',
    'send_whatsapp_message',
    'make_phone_call',
    
    # System Information
    'get_system_info',
    'check_mac_permissions',
    'get_downloads_info',
    
    # Screen Monitoring
    'get_screen_info',
    'get_open_windows_info',
    'get_browser_tabs_detailed',
    
    # Advanced Mac Control
    'toggle_wifi',
    'toggle_bluetooth',
    'toggle_dark_mode',
    'set_audio_output',
    'start_screen_saver',
    'set_keyboard_backlight',
    
    # Web Browser Tools
    'open_website',
    'search_in_browser',
    'open_web_search',
    'control_browser_music',
    
    # Calendar and Reminders
    'get_calendar_events',
    'create_reminder',
    
    # Smart Home
    'control_smart_home',
    
    # File Search
    'find_and_replace_in_file',
    'search_in_files',
    
    # Language Tools
    'detect_language',
    
    # Advanced System Tools
    'set_volume_precise',
    'set_brightness_precise',
    'open_folder_in_app',
    'change_wallpaper',
    
    # Complex AI Tools
    'enhanced_internet_query',
    'multi_source_analysis',
    
    # Automation Tools
    'create_workflow',
    'batch_file_operations',
    'system_health_check',
    'smart_automation',
    
    # Tools Manager
    'get_all_tools',
    'get_tools_description'
] 