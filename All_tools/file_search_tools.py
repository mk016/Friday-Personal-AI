import logging
import os
import re
from livekit.agents import function_tool, RunContext

@function_tool()
async def find_and_replace_in_file(
    context: RunContext,  # type: ignore
    file_path: str,
    find_text: str,
    replace_text: str,
    case_sensitive: bool = True
) -> str:
    """
    Find and replace text in a file
    
    Args:
        file_path: Path of file to edit
        find_text: Text to find
        replace_text: Text to replace with
        case_sensitive: Whether search is case sensitive
    """
    try:
        logging.info(f"Find and replace in file: {file_path}")
        file_path = os.path.expanduser(file_path)
        
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
        
        if not os.path.isfile(file_path):
            return f"Path is not a file: {file_path}"
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Perform find and replace
        if case_sensitive:
            new_content = content.replace(find_text, replace_text)
            count = content.count(find_text)
        else:
            # Case insensitive replacement
            pattern = re.escape(find_text)
            new_content, count = re.subn(pattern, replace_text, content, flags=re.IGNORECASE)
        
        if count == 0:
            return f"No matches found for '{find_text}' in {file_path}"
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return f"Replaced {count} occurrence(s) of '{find_text}' with '{replace_text}' in {file_path}"
        
    except Exception as e:
        logging.error(f"Error in find and replace: {e}")
        return f"Error in find and replace: {str(e)}"

@function_tool()
async def search_in_files(
    context: RunContext,  # type: ignore
    folder_path: str,
    search_text: str,
    file_extension: str = "",
    case_sensitive: bool = True
) -> str:
    """
    Search for text in files within a folder
    
    Args:
        folder_path: Path to search in
        search_text: Text to search for
        file_extension: File extension to filter (e.g., ".txt", ".py")
        case_sensitive: Whether search is case sensitive
    """
    try:
        logging.info(f"Searching for '{search_text}' in {folder_path}")
        folder_path = os.path.expanduser(folder_path)
        
        if not os.path.exists(folder_path):
            return f"Folder not found: {folder_path}"
        
        if not os.path.isdir(folder_path):
            return f"Path is not a folder: {folder_path}"
        
        matches = []
        search_term = search_text if case_sensitive else search_text.lower()
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # Filter by extension if specified
                if file_extension and not file.endswith(file_extension):
                    continue
                
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line_num, line in enumerate(f, 1):
                            line_content = line.rstrip('\n\r')
                            search_in = line_content if case_sensitive else line_content.lower()
                            
                            if search_term in search_in:
                                relative_path = os.path.relpath(file_path, folder_path)
                                matches.append((relative_path, line_num, line_content))
                                
                except (UnicodeDecodeError, PermissionError):
                    continue  # Skip binary files and files without permission
        
        if not matches:
            ext_info = f" (*.{file_extension})" if file_extension else ""
            return f"No matches found for '{search_text}' in {folder_path}{ext_info}"
        
        result = f"Search results for '{search_text}' in {folder_path}:\n"
        result += "=" * 60 + "\n"
        
        for file_path, line_num, line_content in matches[:20]:  # Limit to 20 results
            result += f"File: {file_path} (line {line_num}): {line_content.strip()}\n"
        
        if len(matches) > 20:
            result += f"\n... and {len(matches) - 20} more matches"
        
        result += f"\n\nTotal matches: {len(matches)}"
        return result
        
    except Exception as e:
        logging.error(f"Error searching in files: {e}")
        return f"Error searching in files: {str(e)}" 