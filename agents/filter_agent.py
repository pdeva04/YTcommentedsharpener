"""
Filter Agent - Filters out spam, rude comments, or simple "thanks" messages.

This agent decides whether a comment is worthy of a response.
If the comment should be ignored, it outputs "IGNORE".
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types


def create_filter_agent(retry_config: types.HttpRetryOptions) -> LlmAgent:
    """
    Creates the Filter Agent that checks if a comment is worthy of response.
    
    The agent will:
    - Reject spam comments
    - Reject rude/offensive comments
    - Reject simple "thanks" or "great video" without substance
    - Accept meaningful questions or praise
    
    Args:
        retry_config: HTTP retry configuration for API calls
    
    Returns:
        Configured LlmAgent for filtering comments
    """
    filter_agent = LlmAgent(
        name="FilterAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""You are a comment filter for a YouTube channel.
        
        Your job is to decide if a comment is worthy of a response.
        
        REJECT and output ONLY "IGNORE" if the comment is:
        - Spam or promotional content
        - Rude, offensive, or inappropriate
        - Completely empty or just emojis with no text
        
        ACCEPT and output "ACCEPT" if the comment:
        - Asks a genuine question (even simple ones)
        - Provides praise, appreciation, or positive feedback (even simple "thanks" or "great video")
        - Shares personal experience or story
        - Requests help or clarification
        - Expresses gratitude or compliments
        
        IMPORTANT: 
        - You must output ONLY "IGNORE" or "ACCEPT" - nothing else
        - Be VERY lenient - ACCEPT almost everything except spam/rude comments
        - ACCEPT praise comments - even simple ones like "thanks" or "great video" deserve a response
        - Only reject clearly spam/rude/inappropriate comments
        """,
        output_key="filter_decision"  # Store decision in session state
    )
    
    return filter_agent

