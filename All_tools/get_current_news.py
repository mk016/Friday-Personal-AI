import logging
from livekit.agents import function_tool, RunContext
from ddgs import DDGS
from datetime import datetime

@function_tool()
async def get_current_news(
    context: RunContext,  # type: ignore
    topic: str = "general"
) -> str:
    """
    Get current news and updates on any topic.
    Args:
        topic: News category or specific topic (e.g. "technology", "sports", "India", "business")
    """
    try:
        logging.info(f"Getting current news for: {topic}")
        search_query = f"latest {topic} news today 2024"
        with DDGS() as ddgs:
            results = list(ddgs.news(search_query, max_results=5))
        if results:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            formatted_result = f"📰 Current News - {topic.title()} (as of {current_time}):\n\n"
            for i, result in enumerate(results[:3], 1):
                title = result.get('title', 'No title')
                body = result.get('body', 'No description')
                date = result.get('date', 'Recent')
                url = result.get('url', '')
                formatted_result += f"{i}. **{title}**\n"
                formatted_result += f"   📅 {date}\n"
                formatted_result += f"   {body[:150]}...\n"
                if url:
                    formatted_result += f"   🔗 {url}\n\n"
            logging.info(f"News retrieval successful for: {topic}")
            return formatted_result
        else:
            return f"माफ कीजिए, {topic} के बारे में कोई ताजा खबर नहीं मिली। / Sorry, couldn't find recent news about {topic}."
    except Exception as e:
        logging.error(f"Error getting news: {e}")
        return f"न्यूज़ लाने में समस्या हुई। / Error getting news: {str(e)}" 