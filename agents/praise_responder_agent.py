"""
Praise Responder Agent - Generates thank-you responses for praise comments.

This agent uses the gold_standard.json file to learn the response style
and generates appropriate thank-you messages.
"""

import json
import os
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types


def load_gold_standard() -> str:
    """
    Loads the gold standard responses from JSON file.
    
    Returns:
        Formatted string of example responses for the agent to learn from
    """
    try:
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        gold_standard_path = os.path.join(current_dir, "data", "gold_standard.json")
        
        with open(gold_standard_path, "r", encoding="utf-8") as f:
            gold_data = json.load(f)
        
        # Format examples for the agent
        examples = []
        for item in gold_data:
            examples.append(f"Comment: {item['input_comment']}\nReply: {item['your_response']}")
        
        return "\n\n".join(examples)
    except Exception as e:
        return f"Error loading gold standard: {str(e)}"


def create_praise_responder_agent(retry_config: types.HttpRetryOptions) -> LlmAgent:
    """
    Creates the Praise Responder Agent that generates thank-you responses.
    
    The agent learns from gold_standard.json to match the channel's response style:
    - Friendly and casual tone
    - Mix of Hindi and English (Hinglish)
    - Appreciative and warm
    - Sometimes includes emojis
    
    Args:
        retry_config: HTTP retry configuration for API calls
    
    Returns:
        Configured LlmAgent for responding to praise
    """
    # Load style examples
    style_examples = load_gold_standard()
    
    praise_agent = LlmAgent(
        name="PraiseResponderAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction=f"""You are a YouTube channel comment responder. Your job is to write thank-you responses to praise comments.

STYLE GUIDE (learn from these examples - this is YOUR ACTUAL RESPONSE STYLE):
{style_examples}

CRITICAL STYLE RULES (match the examples above exactly):
1. Use Hinglish (mix of Hindi and English) naturally - like the examples show
2. Keep responses SHORT and casual (1-2 sentences max)
3. Be warm but not overly formal
4. Match the tone - if they use "bhaiy", "sir", respond in kind
5. Use emojis when appropriate (⭐️, 😂) but sparingly
6. Be genuine and personal - like talking to a friend
7. For simple "thanks" or "thank you", respond warmly but briefly
8. Look at the examples - notice how casual and Hinglish they are

EXAMPLES OF GOOD RESPONSES:
- "Thanks bhaiy for this" → "That's the spirit! ⭐️"
- "Thank You Sir!" → "You are most welcome!"
- "Great video!" → "Glad it helped! 😊"

TASK:
- Read the user's praise comment
- Write a thank-you response matching the style in the examples above
- Use Hinglish naturally
- Keep it short and warm
- Match their energy level

Output ONLY your response - no explanations or meta-commentary.
        """,
        output_key="praise_response"  # Store response in session state
    )
    
    return praise_agent

