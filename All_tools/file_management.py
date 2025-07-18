import logging
import os
import shutil
import subprocess
from datetime import datetime
from livekit.agents import function_tool, RunContext

@function_tool()
async def create_file(
    context: RunContext,  # type: ignore
    file_path: str,
    content: str = "",
    overwrite: bool = False
) -> str:
    """
    Create a new file with optional content
    
    Args:
        file_path: Path where to create the file (e.g., "~/Documents/myfile.txt")
        content: Initial content for the file (optional)
        overwrite: Whether to overwrite if file exists
    """
    try:
        logging.info(f"Creating file: {file_path}")
        file_path = os.path.expanduser(file_path)
        
        # Check if file exists
        if os.path.exists(file_path) and not overwrite:
            return f"File already exists at {file_path}. Use overwrite=True to replace it."
        
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Create file with content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"✅ File created successfully: {file_path}"
        
    except Exception as e:
        logging.error(f"Error creating file: {e}")
        return f"❌ Error creating file: {str(e)}"

@function_tool()
async def delete_file(
    context: RunContext,  # type: ignore
    file_path: str,
    permanent: bool = False
) -> str:
    """
    Delete a file (moves to trash by default for safety)
    
    Args:
        file_path: Path of file to delete
        permanent: Whether to delete permanently (default: move to trash)
    """
    try:
        logging.info(f"Deleting file: {file_path}")
        file_path = os.path.expanduser(file_path)
        
        if not os.path.exists(file_path):
            return f"❌ File not found: {file_path}"
        
        if not os.path.isfile(file_path):
            return f"❌ Path is not a file: {file_path}"
        
        # Move to trash instead of permanent deletion (safer)
        if not permanent:
            subprocess.run(['osascript', '-e', f'tell application "Finder" to delete POSIX file "{file_path}"'], 
                          check=True, capture_output=True)
            return f"🗑️ File moved to trash: {file_path}"
        else:
            os.remove(file_path)
            return f"✅ File deleted permanently: {file_path}"
        
    except Exception as e:
        logging.error(f"Error deleting file: {e}")
        return f"❌ Error deleting file: {str(e)}"

@function_tool()
async def read_file_content(
    context: RunContext,  # type: ignore
    file_path: str,
    start_line: int = 1,
    end_line: int = None
) -> str:
    """
    Read content from a file (optionally specific lines)
    
    Args:
        file_path: Path of file to read
        start_line: Starting line number (1-based)
        end_line: Ending line number (inclusive), if None reads entire file
    """
    try:
        logging.info(f"Reading file: {file_path}")
        file_path = os.path.expanduser(file_path)
        
        if not os.path.exists(file_path):
            return f"❌ File not found: {file_path}"
        
        if not os.path.isfile(file_path):
            return f"❌ Path is not a file: {file_path}"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # If specific lines requested
        if end_line is not None:
            if start_line < 1 or start_line > len(lines):
                return f"❌ Invalid start line: {start_line}. File has {len(lines)} lines."
            
            if end_line > len(lines):
                end_line = len(lines)
            
            selected_lines = lines[start_line - 1:end_line]
            content = ''.join(selected_lines)
            return f"📄 Lines {start_line}-{end_line} from {file_path}:\n\n{content}"
        else:
            content = ''.join(lines)
            file_size = os.path.getsize(file_path)
            return f"📄 File: {file_path}\n📏 Size: {file_size} bytes\n\n{content}"
        
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        return f"❌ Error reading file: {str(e)}"

@function_tool()
async def write_file_content(
    context: RunContext,  # type: ignore
    file_path: str,
    content: str,
    append: bool = False
) -> str:
    """
    Write content to a file
    
    Args:
        file_path: Path of file to write
        content: Content to write
        append: Whether to append (True) or overwrite (False)
    """
    try:
        logging.info(f"Writing to file: {file_path}")
        file_path = os.path.expanduser(file_path)
        
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        mode = 'a' if append else 'w'
        with open(file_path, mode, encoding='utf-8') as f:
            f.write(content)
        
        action = "appended to" if append else "written to"
        return f"✅ Content {action} file: {file_path}"
        
    except Exception as e:
        logging.error(f"Error writing to file: {e}")
        return f"❌ Error writing to file: {str(e)}"

@function_tool()
async def create_folder(
    context: RunContext,  # type: ignore
    folder_path: str
) -> str:
    """
    Create a new folder (including parent directories if needed)
    
    Args:
        folder_path: Path where to create the folder (e.g., "~/Documents/MyProject")
    """
    try:
        logging.info(f"Creating folder: {folder_path}")
        folder_path = os.path.expanduser(folder_path)
        
        if os.path.exists(folder_path):
            if os.path.isdir(folder_path):
                return f"📁 Folder पहले से मौजूद है: {folder_path}"
            else:
                return f"❌ यहाँ एक file है, folder नहीं: {folder_path}"
        
        # Create parent directories if needed
        parent_dir = os.path.dirname(folder_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
            logging.info(f"Created parent directories: {parent_dir}")
        
        # Create the target folder
        os.makedirs(folder_path, exist_ok=False)  # Don't use exist_ok=True to catch actual creation
        
        return f"✅ Folder बनाया गया successfully: {folder_path}"
        
    except FileExistsError:
        return f"📁 Folder पहले से exists करता है: {folder_path}"
    except PermissionError:
        return f"❌ Permission denied: {folder_path} बनाने की अनुमति नहीं है"
    except Exception as e:
        logging.error(f"Error creating folder: {e}")
        return f"❌ Folder बनाने में error: {str(e)}"

@function_tool()
async def list_folder_contents(
    context: RunContext,  # type: ignore
    folder_path: str,
    show_hidden: bool = False,
    detailed: bool = False
) -> str:
    """
    List contents of a folder
    
    Args:
        folder_path: Path of folder to list
        show_hidden: Whether to show hidden files/folders
        detailed: Whether to show detailed information (size, date)
    """
    try:
        logging.info(f"Listing folder contents: {folder_path}")
        folder_path = os.path.expanduser(folder_path)
        
        if not os.path.exists(folder_path):
            return f"❌ Folder not found: {folder_path}"
        
        if not os.path.isdir(folder_path):
            return f"❌ Path is not a folder: {folder_path}"
        
        items = os.listdir(folder_path)
        
        # Filter hidden files if requested
        if not show_hidden:
            items = [item for item in items if not item.startswith('.')]
        
        if not items:
            return f"📁 Folder is empty: {folder_path}"
        
        # Sort items: folders first, then files
        folders = []
        files = []
        
        for item in sorted(items):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                folders.append(item)
            else:
                files.append(item)
        
        result = f"📁 Contents of: {folder_path}\n"
        result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        # List folders first
        if folders:
            result += "📂 Folders:\n"
            for folder in folders:
                if detailed:
                    folder_path_full = os.path.join(folder_path, folder)
                    stat_info = os.stat(folder_path_full)
                    modified_time = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M')
                    result += f"  📁 {folder:<30} {modified_time}\n"
                else:
                    result += f"  📁 {folder}\n"
            result += "\n"
        
        # List files
        if files:
            result += "📄 Files:\n"
            for file in files:
                if detailed:
                    file_path_full = os.path.join(folder_path, file)
                    stat_info = os.stat(file_path_full)
                    file_size = stat_info.st_size
                    modified_time = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M')
                    
                    # Format file size
                    if file_size < 1024:
                        size_str = f"{file_size}B"
                    elif file_size < 1024 * 1024:
                        size_str = f"{file_size / 1024:.1f}KB"
                    elif file_size < 1024 * 1024 * 1024:
                        size_str = f"{file_size / (1024 * 1024):.1f}MB"
                    else:
                        size_str = f"{file_size / (1024 * 1024 * 1024):.1f}GB"
                    
                    result += f"  📄 {file:<25} {size_str:<8} {modified_time}\n"
                else:
                    result += f"  📄 {file}\n"
        
        result += f"\n📊 Total: {len(folders)} folders, {len(files)} files"
        return result
        
    except Exception as e:
        logging.error(f"Error listing folder contents: {e}")
        return f"❌ Folder contents लिस्ट करने में error: {str(e)}"

@function_tool()
async def copy_file_or_folder(
    context: RunContext,  # type: ignore
    source_path: str,
    destination_path: str,
    overwrite: bool = False
) -> str:
    """
    Copy a file or folder to another location
    
    Args:
        source_path: Path of source file/folder
        destination_path: Path where to copy
        overwrite: Whether to overwrite if destination exists
    """
    try:
        logging.info(f"Copying: {source_path} to {destination_path}")
        source_path = os.path.expanduser(source_path)
        destination_path = os.path.expanduser(destination_path)
        
        if not os.path.exists(source_path):
            return f"❌ Source not found: {source_path}"
        
        if os.path.exists(destination_path) and not overwrite:
            return f"❌ Destination already exists: {destination_path}. Use overwrite=True to replace."
        
        # Remove destination if overwriting
        if os.path.exists(destination_path) and overwrite:
            if os.path.isdir(destination_path):
                shutil.rmtree(destination_path)
            else:
                os.remove(destination_path)
        
        # Create destination directory if needed
        dest_dir = os.path.dirname(destination_path)
        if dest_dir:
            os.makedirs(dest_dir, exist_ok=True)
        
        # Copy file or folder
        if os.path.isdir(source_path):
            shutil.copytree(source_path, destination_path)
            return f"✅ Folder copied: {source_path} → {destination_path}"
        else:
            shutil.copy2(source_path, destination_path)
            return f"✅ File copied: {source_path} → {destination_path}"
        
    except Exception as e:
        logging.error(f"Error copying: {e}")
        return f"❌ Error copying: {str(e)}"

@function_tool()
async def move_file_or_folder(
    context: RunContext,  # type: ignore
    source_path: str,
    destination_path: str,
    overwrite: bool = False
) -> str:
    """
    Move a file or folder to another location
    
    Args:
        source_path: Path of source file/folder
        destination_path: Path where to move
        overwrite: Whether to overwrite if destination exists
    """
    try:
        logging.info(f"Moving: {source_path} to {destination_path}")
        source_path = os.path.expanduser(source_path)
        destination_path = os.path.expanduser(destination_path)
        
        if not os.path.exists(source_path):
            return f"❌ Source not found: {source_path}"
        
        if os.path.exists(destination_path) and not overwrite:
            return f"❌ Destination already exists: {destination_path}. Use overwrite=True to replace."
        
        # Remove destination if overwriting
        if os.path.exists(destination_path) and overwrite:
            if os.path.isdir(destination_path):
                shutil.rmtree(destination_path)
            else:
                os.remove(destination_path)
        
        # Create destination directory if needed
        dest_dir = os.path.dirname(destination_path)
        if dest_dir:
            os.makedirs(dest_dir, exist_ok=True)
        
        # Move file or folder
        shutil.move(source_path, destination_path)
        
        item_type = "Folder" if os.path.isdir(destination_path) else "File"
        return f"✅ {item_type} moved: {source_path} → {destination_path}"
        
    except Exception as e:
        logging.error(f"Error moving: {e}")
        return f"❌ Error moving: {str(e)}" 