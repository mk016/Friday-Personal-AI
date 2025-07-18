import logging
import subprocess
import os
import platform
from livekit.agents import function_tool, RunContext
from typing import List, Dict

def is_mac():
    """Check if running on Mac"""
    return platform.system() == "Darwin"

@function_tool()
async def create_workflow(
    context: RunContext,  # type: ignore
    workflow_name: str,
    steps: List[Dict]
) -> str:
    """
    Create and execute a workflow of multiple actions.
    Args:
        workflow_name: Name of the workflow
        steps: List of steps with action and parameters
    """
    try:
        logging.info(f"Creating workflow: {workflow_name}")
        
        results = []
        
        for i, step in enumerate(steps, 1):
            action = step.get('action')
            params = step.get('params', {})
            
            # Execute the action based on type
            if action == 'open_app':
                from .application_control import open_app
                result = await open_app(context, params.get('app_name', ''))
            elif action == 'search_internet':
                from .search_internet import search_internet
                result = await search_internet(context, params.get('query', ''))
            elif action == 'create_file':
                from .file_management import create_file
                result = await create_file(context, params.get('file_path', ''), params.get('content', ''))
            elif action == 'send_email':
                from .communication_tools import send_email
                result = await send_email(context, params.get('to_email', ''), params.get('subject', ''), params.get('message', ''))
            else:
                result = f"Unknown action: {action}"
            
            results.append(f"Step {i} ({action}): {result}")
        
        return f"Workflow '{workflow_name}' completed:\n" + "\n".join(results)
        
    except Exception as e:
        logging.error(f"Error in workflow: {e}")
        return f"Workflow error: {str(e)}"

@function_tool()
async def batch_file_operations(
    context: RunContext,  # type: ignore
    operation: str,
    source_folder: str,
    file_pattern: str = "*",
    destination: str = ""
) -> str:
    """
    Perform batch operations on files.
    Args:
        operation: Operation to perform (copy, move, delete, rename)
        source_folder: Source folder path
        file_pattern: File pattern to match
        destination: Destination folder (for copy/move)
    """
    try:
        logging.info(f"Batch file operation: {operation} on {source_folder}")
        
        from .file_management import copy_file_or_folder, move_file_or_folder, delete_file
        
        results = []
        
        if operation == "copy":
            for file in os.listdir(source_folder):
                if file_pattern == "*" or file.endswith(file_pattern):
                    result = await copy_file_or_folder(context, f"{source_folder}/{file}", f"{destination}/{file}")
                    results.append(result)
        elif operation == "move":
            for file in os.listdir(source_folder):
                if file_pattern == "*" or file.endswith(file_pattern):
                    result = await move_file_or_folder(context, f"{source_folder}/{file}", f"{destination}/{file}")
                    results.append(result)
        elif operation == "delete":
            for file in os.listdir(source_folder):
                if file_pattern == "*" or file.endswith(file_pattern):
                    result = await delete_file(context, f"{source_folder}/{file}")
                    results.append(result)
        
        return f"Batch {operation} completed:\n" + "\n".join(results)
        
    except Exception as e:
        logging.error(f"Error in batch operation: {e}")
        return f"Batch operation error: {str(e)}"

@function_tool()
async def system_health_check(
    context: RunContext,  # type: ignore
) -> str:
    """
    Perform a comprehensive system health check.
    """
    try:
        logging.info("Performing system health check")
        
        if not is_mac():
            return "System health check is only available on macOS."
        
        results = []
        
        # Check battery
        try:
            from .system_info_tools import get_system_info
            battery_info = await get_system_info(context, "battery")
            results.append(f"🔋 Battery: {battery_info}")
        except:
            results.append(" Battery: Could not retrieve")
        
        # Check storage
        try:
            storage_info = await get_system_info(context, "storage")
            results.append(f"💾 Storage: {storage_info}")
        except:
            results.append(" Storage: Could not retrieve")
        
        # Check permissions
        try:
            from .system_info_tools import check_mac_permissions
            perm_info = await check_mac_permissions(context)
            results.append(f" Permissions: {perm_info}")
        except:
            results.append(" Permissions: Could not check")
        
        # Check running applications
        try:
            from .screen_monitoring import get_screen_info
            screen_info = await get_screen_info(context)
            results.append(f"📱 Applications: {screen_info}")
        except:
            results.append("📱 Applications: Could not retrieve")
        
        return "System Health Check Results:\n" + "\n".join(results)
        
    except Exception as e:
        logging.error(f"Error in system health check: {e}")
        return f"System health check error: {str(e)}"

@function_tool()
async def smart_automation(
    context: RunContext,  # type: ignore
    task_description: str
) -> str:
    """
    Automatically determine and execute the best actions for a given task.
    Args:
        task_description: Description of what needs to be done
    """
    try:
        logging.info(f"Smart automation for: {task_description}")
        
        task_lower = task_description.lower()
        results = []
        
        # Analyze task and determine actions
        if "email" in task_lower or "mail" in task_lower:
            results.append("📧 Email task detected - use send_email tool")
        
        if "search" in task_lower or "find" in task_lower:
            results.append("🔍 Search task detected - use search_internet tool")
        
        if "weather" in task_lower:
            results.append("🌤️ Weather task detected - use get_weather_info tool")
        
        if "news" in task_lower:
            results.append(" News task detected - use get_current_news tool")
        
        if "file" in task_lower or "folder" in task_lower:
            results.append(" File task detected - use file management tools")
        
        if "music" in task_lower or "play" in task_lower:
            results.append("🎵 Music task detected - use control_music tool")
        
        if "app" in task_lower or "open" in task_lower:
            results.append("📱 App task detected - use open_app tool")
        
        if "brightness" in task_lower or "volume" in task_lower:
            results.append("⚙️ System control task detected - use system control tools")
        
        if not results:
            results.append("🤖 Complex task detected - use enhanced_internet_query for analysis")
        
        return f"Smart Automation Analysis:\n" + "\n".join(results)
        
    except Exception as e:
        logging.error(f"Error in smart automation: {e}")
        return f"Smart automation error: {str(e)}" 