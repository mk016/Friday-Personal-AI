import logging
import re
from livekit.agents import function_tool, RunContext

# Language detection patterns
HINDI_PATTERNS = [
    r'[\u0900-\u097F]+',  # Devanagari script
    r'\b(नमस्ते|हैलो|हाय|कैसे|क्या|कहाँ|कब|कौन|क्यों|हाँ|नहीं|धन्यवाद|कृपया|जी|सर|बॉस)\b'
]

ENGLISH_PATTERNS = [
    r'\b(hello|hi|hey|what|when|where|why|how|yes|no|thanks|thank|you|please|can|could|would|should|will|do|does|did|am|is|are|was|were|have|has|had|sir|boss)\b'
]

@function_tool()
async def detect_language(
    context: RunContext,  # type: ignore
    text: str) -> str:
    """
    Detect if the text is in English or Hindi.
    Returns 'hindi', 'english', or 'unknown'.
    """
    try:
        text_lower = text.lower()
        
        # Check for Hindi patterns
        hindi_score = 0
        for pattern in HINDI_PATTERNS:
            if re.search(pattern, text):
                hindi_score += 1
        
        # Check for English patterns  
        english_score = 0
        for pattern in ENGLISH_PATTERNS:
            if re.search(pattern, text_lower):
                english_score += 1
        
        if hindi_score > english_score:
            return "hindi"
        elif english_score > hindi_score:
            return "english"
        else:
            # Default to English if uncertain
            return "english"
            
    except Exception as e:
        logging.error(f"Error detecting language: {e}")
        return "english"  # Default fallback 