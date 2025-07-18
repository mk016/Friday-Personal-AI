import logging
import requests
import os
from livekit.agents import function_tool, RunContext
from typing import Optional
import json
from datetime import datetime

# Initialize API clients
cloud_api_key = os.getenv("CLOUD_API_KEY")
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

@function_tool()
async def enhanced_internet_query(
    context: RunContext,  # type: ignore
    query: str,
    analysis_type: str = "comprehensive"
) -> str:
    """
    Enhanced internet query with multiple sources and analysis.
    Args:
        query: The question or topic to research
        analysis_type: Type of analysis (comprehensive, summary, detailed)
    """
    try:
        logging.info(f"Enhanced internet query: {query}")
        
        # Get information from multiple sources
        from .search_internet import search_internet
        from .get_current_news import get_current_news
        
        # Get basic search results
        search_results = await search_internet(context, query)
        
        # Get related news
        news_results = await get_current_news(context, query)
        
        # Combine and analyze
        combined_info = f"""
SEARCH RESULTS:
{search_results}

RELATED NEWS:
{news_results}
"""
        
        # Use AI to analyze and summarize
        if analysis_type == "comprehensive":
            return await ask_cloud_api_with_internet(context, f"Analyze this information comprehensively: {combined_info}")
        elif analysis_type == "summary":
            return await ask_deepseek_with_internet(context, f"Provide a concise summary: {combined_info}")
        else:
            return combined_info
            
    except Exception as e:
        logging.error(f"Error in enhanced internet query: {e}")
        return f"Error in enhanced query: {str(e)}"

@function_tool()
async def multi_source_analysis(
    context: RunContext,  # type: ignore
    topic: str,
    sources: str = "all"
) -> str:
    """
    Get analysis from multiple sources (news, weather, social media, etc.)
    Args:
        topic: Topic to analyze
        sources: Which sources to use (all, news, weather, social)
    """
    try:
        logging.info(f"Multi-source analysis for: {topic}")
        
        results = []
        
        if sources in ["all", "news"]:
            news = await get_current_news(context, topic)
            results.append(f"NEWS: {news}")
        
        if sources in ["all", "weather"]:
            weather = await get_weather_info(context, topic)
            results.append(f"WEATHER: {weather}")
        
        if sources in ["all", "search"]:
            search = await search_internet(context, topic)
            results.append(f"SEARCH: {search}")
        
        combined = "\n\n".join(results)
        
        # Use AI to synthesize
        return await ask_cloud_api_with_internet(context, f"Synthesize this multi-source information about {topic}: {combined}")
        
    except Exception as e:
        logging.error(f"Error in multi-source analysis: {e}")
        return f"Error in analysis: {str(e)}" 