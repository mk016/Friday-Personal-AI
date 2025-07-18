import logging
from livekit.agents import function_tool, RunContext
from ddgs import DDGS
from datetime import datetime

@function_tool()
async def get_weather_info(
    context: RunContext,  # type: ignore,
    location: str = "current location"
) -> str:
    """
    Get current weather information for any location.
    Args:
        location: City or location name (e.g. "Delhi", "Mumbai", "New York")
    """
    try:
        logging.info(f"Getting weather for: {location}")
        search_query = f"weather {location} today current temperature forecast"
        with DDGS() as ddgs:
            results = list(ddgs.text(search_query, max_results=3))
        if results:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            formatted_result = f"🌤️ Weather Update for {location.title()} (as of {current_time}):\n\n"
            for i, result in enumerate(results[:2], 1):
                title = result.get('title', 'No title')
                body = result.get('body', 'No description')
                if 'weather' in title.lower() or 'temperature' in body.lower():
                    formatted_result += f"{i}. **{title}**\n"
                    formatted_result += f"   {body[:200]}...\n\n"
            logging.info(f"Weather retrieval successful for: {location}")
            return formatted_result
        else:
            return f"माफ कीजिए, {location} के मौसम की जानकारी नहीं मिली। / Sorry, couldn't get weather information for {location}."
    except Exception as e:
        logging.error(f"Error getting weather: {e}")
        return f"मौसम की जानकारी लाने में समस्या हुई। / Error getting weather: {str(e)}" 