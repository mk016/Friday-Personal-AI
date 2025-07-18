import logging
import subprocess
import os
import platform
from livekit.agents import function_tool, RunContext

def is_mac():
    """Check if running on Mac"""
    return platform.system() == "Darwin"

@function_tool()
async def get_system_info(
    context: RunContext,  # type: ignore
    info_type: str = "general"
) -> str:
    """
    Get Mac system information (battery, storage, memory, date/time, etc.).
    Args:
        info_type: Type of info (battery, storage, memory, date, time, general)
    """
    try:
        logging.info(f"Getting system info: {info_type}")
        
        if not is_mac():
            return "यह फीचर केवल Mac पर उपलब्ध है। / This feature is only available on Mac."
        
        if info_type == "battery":
            result = subprocess.run(['pmset', '-g', 'batt'], capture_output=True, text=True)
            if result.returncode == 0:
                battery_info = result.stdout
                # Extract battery percentage
                import re
                match = re.search(r'(\d+)%', battery_info)
                if match:
                    percentage = match.group(1)
                    return f"🔋 Battery: {percentage}% - {battery_info.split(';')[1].strip() if ';' in battery_info else 'Status unknown'}"
            
        elif info_type == "storage":
            result = subprocess.run(['df', '-h'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if '/' in line and not line.startswith('Filesystem'):
                        parts = line.split()
                        if len(parts) >= 4:
                            return f"💾 Storage: {parts[3]} available out of {parts[1]} total"
        
        elif info_type == "memory":
            result = subprocess.run(['vm_stat'], capture_output=True, text=True)
            if result.returncode == 0:
                return f"🧠 Memory info retrieved - {result.stdout[:100]}..."
        
        elif info_type == "date":
            result = subprocess.run(['date'], capture_output=True, text=True)
            if result.returncode == 0:
                return f"�� Current date/time: {result.stdout.strip()}"
        
        elif info_type == "general":
            result = subprocess.run(['system_profiler', 'SPHardwareDataType'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')[:10]
                return f"�� System Info: {' '.join(lines)[:200]}..."
        
        return f"System information के लिए: {info_type}"
        
    except Exception as e:
        logging.error(f"Error getting system info: {e}")
        return f"System info में error: {str(e)}"

@function_tool()
async def check_mac_permissions(
    context: RunContext,  # type: ignore
) -> str:
    """
    Check if Terminal has required permissions for Mac control and provide setup instructions
    """
    if not is_mac():
        return "This function is only supported on macOS."
    
    permissions_status = []
    
    # Test Accessibility permission
    try:
        test_script = '''
        tell application "System Events"
            return true
        end tell
        '''
        subprocess.run(["osascript", "-e", test_script], check=True, capture_output=True)
        permissions_status.append("✅ Accessibility: Enabled")
    except subprocess.CalledProcessError:
        permissions_status.append("❌ Accessibility: DISABLED")
    
    status_report = "\n".join(permissions_status)
    
    setup_instructions = """

�� SETUP INSTRUCTIONS:

1. ACCESSIBILITY PERMISSIONS:
   • Open System Settings > Privacy & Security > Accessibility
   • Click the + button
   • Add Terminal and turn it ON

2. AUTOMATION PERMISSIONS:
   • Open System Settings > Privacy & Security > Automation
   • Find Terminal in the list
   • Enable: System Events, Safari, and other apps you want to control
"""
    
    return status_report + setup_instructions

@function_tool()
async def get_downloads_info(
    context: RunContext,  # type: ignore
) -> str:
    """
    Get detailed information about Downloads folder contents
    """
    try:
        downloads_path = os.path.expanduser("~/Downloads")
        logging.info(f"Getting Downloads folder info: {downloads_path}")
        
        if not os.path.exists(downloads_path):
            return f"❌ Downloads folder नहीं मिला: {downloads_path}"
        
        # Get all items
        items = os.listdir(downloads_path)
        
        if not items:
            return f"�� Downloads folder खाली है"
        
        # Categorize items
        folders = []
        images = []
        documents = []
        videos = []
        music = []
        apps = []
        other_files = []
        
        # File extension mapping
        image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic'}
        doc_exts = {'.pdf', '.doc', '.docx', '.txt', '.rtf', '.pages', '.xlsx', '.xls', '.ppt', '.pptx'}
        video_exts = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.m4v', '.flv'}
        music_exts = {'.mp3', '.m4a', '.wav', '.flac', '.aac', '.ogg'}
        app_exts = {'.dmg', '.pkg', '.app', '.zip', '.rar', '.7z'}
        
        for item in items:
            item_path = os.path.join(downloads_path, item)
            
            if os.path.isdir(item_path):
                folders.append(item)
            else:
                _, ext = os.path.splitext(item.lower())
                
                if ext in image_exts:
                    images.append(item)
                elif ext in doc_exts:
                    documents.append(item)
                elif ext in video_exts:
                    videos.append(item)
                elif ext in music_exts:
                    music.append(item)
                elif ext in app_exts:
                    apps.append(item)
                else:
                    other_files.append(item)
        
        # Build result
        result = f"📁 Downloads Folder Analysis:\n"
        result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        # Summary
        total_items = len(items)
        result += f"📊 कुल Items: {total_items}\n\n"
        
        # Categories
        if folders:
            result += f"�� Folders ({len(folders)}):\n"
            for folder in sorted(folders)[:10]:  # Show max 10
                result += f"  📁 {folder}\n"
            if len(folders) > 10:
                result += f"  ... और {len(folders) - 10} folders\n"
            result += "\n"
        
        if images:
            result += f"🖼️ Images ({len(images)}):\n"
            for img in sorted(images)[:5]:
                result += f"  🖼️ {img}\n"
            if len(images) > 5:
                result += f"  ... और {len(images) - 5} images\n"
            result += "\n"
        
        if documents:
            result += f"📄 Documents ({len(documents)}):\n"
            for doc in sorted(documents)[:5]:
                result += f"  📄 {doc}\n"
            if len(documents) > 5:
                result += f"  ... और {len(documents) - 5} documents\n"
            result += "\n"
        
        if videos:
            result += f"🎥 Videos ({len(videos)}):\n"
            for vid in sorted(videos)[:3]:
                result += f"  🎥 {vid}\n"
            if len(videos) > 3:
                result += f"  ... और {len(videos) - 3} videos\n"
            result += "\n"
        
        if music:
            result += f"🎵 Music ({len(music)}):\n"
            for mus in sorted(music)[:3]:
                result += f"  🎵 {mus}\n"
            if len(music) > 3:
                result += f"  ... और {len(music) - 3} music files\n"
            result += "\n"
        
        if apps:
            result += f"📦 Apps/Archives ({len(apps)}):\n"
            for app in sorted(apps)[:5]:
                result += f"  📦 {app}\n"
            if len(apps) > 5:
                result += f"  ... और {len(apps) - 5} apps/archives\n"
            result += "\n"
        
        if other_files:
            result += f"📋 Other Files ({len(other_files)}):\n"
            for other in sorted(other_files)[:5]:
                result += f"  📋 {other}\n"
            if len(other_files) > 5:
                result += f"  ... और {len(other_files) - 5} other files\n"
        
        return result
        
    except Exception as e:
        logging.error(f"Error getting downloads info: {e}")
        return f"❌ Downloads info लेने में error: {str(e)}" 