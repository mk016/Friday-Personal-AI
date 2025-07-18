import logging
import requests
import os
from livekit.agents import function_tool, RunContext
from ddgs import DDGS
from datetime import datetime

# Initialize API clients
cloud_api_key = os.getenv("CLOUD_API_KEY")
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

@function_tool()
async def ask_cloud_api_with_internet(
    context: RunContext,  # type: ignore
    question: str
) -> str:
    """
    Ask Cloud API to answer questions with access to current internet information.
    Perfect for complex questions that need updated data and analysis.
    Args:
        question: Any question you want answered with current information
    """
    try:
        logging.info(f"Asking Cloud API with internet context: {question}")
        
        # First get internet search results
        with DDGS() as ddgs:
            search_results = list(ddgs.text(question, max_results=5))
        
        # Format search results for context
        context_info = ""
        for result in search_results[:3]:
            context_info += f"- {result.get('title', '')}: {result.get('body', '')[:200]}...\n"
        
        # Prepare the prompt for Cloud API
        prompt = f"""You are Friday, a personal AI assistant. The user asked: "{question}"

Here is current internet information I found:
{context_info}

Please provide a comprehensive answer using this current information. Respond naturally as Friday would, and if the user's language preference is Hindi, respond in Hindi, otherwise respond in English.

Current time: {datetime.now().strftime("%Y-%m-%d %H:%M")}"""

        # Call Cloud API
        headers = {
            'Authorization': f'Bearer {cloud_api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'claude-4-sonnet-20240229',
            'messages': [
                {"role": "system", "content": "You are Friday, a helpful AI assistant like from Iron Man. Be professional but friendly."},
                {"role": "user", "content": prompt}
            ],
            'max_tokens': 1000,
            'temperature': 0.7
        }
        
        response = requests.post('https://api.claude.ai/v1/chat/completions', 
                               headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            answer = response.json()['choices'][0]['message']['content']
            logging.info(f"Cloud API response successful for: {question}")
            return answer
        else:
            # Fallback to DeepSeek API
            return await ask_deepseek_with_internet(context, question)
        
    except Exception as e:
        logging.error(f"Error with Cloud API internet query: {e}")
        # Fallback to DeepSeek API
        return await ask_deepseek_with_internet(context, question)

@function_tool()
async def ask_deepseek_with_internet(
    context: RunContext,  # type: ignore
    question: str
) -> str:
    """
    Ask DeepSeek API to answer questions with access to current internet information.
    Alternative AI model for complex questions with updated data.
    Args:
        question: Any question you want answered with current information
    """
    try:
        logging.info(f"Asking DeepSeek API with internet context: {question}")
        
        # First get internet search results
        with DDGS() as ddgs:
            search_results = list(ddgs.text(question, max_results=5))
        
        # Format search results for context
        context_info = ""
        for result in search_results[:3]:
            context_info += f"- {result.get('title', '')}: {result.get('body', '')[:200]}...\n"
        
        # Prepare the prompt for DeepSeek API
        prompt = f"""You are Friday, a personal AI assistant. The user asked: "{question}"

Here is current internet information I found:
{context_info}

Please provide a comprehensive answer using this current information. Respond naturally as Friday would, and if the user's language preference is Hindi, respond in Hindi, otherwise respond in English.

Current time: {datetime.now().strftime("%Y-%m-%d %H:%M")}"""

        # Call DeepSeek API
        headers = {
            'Authorization': f'Bearer {deepseek_api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'deepseek-chat',
            'messages': [
                {"role": "system", "content": "You are Friday, a helpful AI assistant like from Iron Man. Be professional but friendly."},
                {"role": "user", "content": prompt}
            ],
            'max_tokens': 1000,
            'temperature': 0.7
        }
        
        response = requests.post('https://api.deepseek.com/v1/chat/completions', 
                               headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            answer = response.json()['choices'][0]['message']['content']
            logging.info(f"DeepSeek API response successful for: {question}")
            return answer
        else:
            # Fallback to simple search
            from .search_internet import search_internet
            return await search_internet(context, question)
        
    except Exception as e:
        logging.error(f"Error with DeepSeek API internet query: {e}")
        # Fallback to simple search
        from .search_internet import search_internet
        return await search_internet(context, question) 