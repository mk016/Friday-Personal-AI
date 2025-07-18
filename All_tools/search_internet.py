import logging
from livekit.agents import function_tool, RunContext
from ddgs import DDGS
from datetime import datetime

@function_tool()
async def search_internet(
    context: RunContext,  # type: ignore
    query: str
) -> str:
    """
    Search the internet for current information on any topic using DuckDuckGo.
    Perfect for getting updated information, news, weather, current events etc.
    Args:
        query: What to search for (e.g. "latest news", "weather in Delhi", "Bitcoin price")
    """
    try:
        logging.info(f"Searching internet for: {query}")
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
        if results:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            formatted_result = f"🔍 Internet Search Results (as of {current_time}):\n\n"
            for i, result in enumerate(results[:3], 1):
                title = result.get('title', 'No title')
                body = result.get('body', 'No description')
                link = result.get('href', '')
                formatted_result += f"{i}. **{title}**\n"
                formatted_result += f"   {body[:150]}...\n"
                if link:
                    formatted_result += f"   🔗 {link}\n\n"
            logging.info(f"Search successful for query: {query}")
            return formatted_result
        else:
            return "माफ कीजिए, मुझे इस विषय पर कोई जानकारी नहीं मिली। / Sorry, I couldn't find any information on this topic."
    except Exception as e:
        logging.error(f"Error searching internet: {e}")
        return f"खोज में समस्या हुई। / Error occurred while searching: {str(e)}" 