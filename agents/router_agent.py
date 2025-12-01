"""
Router Agent - Routes accepted comments to either "Question" or "Praise" handlers.

This agent analyzes the comment and decides if it's a question that needs answering
or praise that needs acknowledgment.
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types


def create_router_agent(retry_config: types.HttpRetryOptions) -> LlmAgent:
    """
    Creates the Router Agent that categorizes comments as "Question" or "Praise".
    
    The agent analyzes the comment and determines:
    - If it's a question (needs information/answer) → "Question"
    - If it's praise/feedback (needs acknowledgment) → "Praise"
    
    Args:
        retry_config: HTTP retry configuration for API calls
    
    Returns:
        Configured LlmAgent for routing comments
    """
    router_agent = LlmAgent(
        name="RouterAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""You are a comment router for a YouTube channel.
        
        Your job is to categorize comments into two types:
        
        Output "Question" if the comment:
        - Asks a question (with "?", "how", "what", "why", "can you", etc.)
        - Requests information or clarification
        - Needs an answer or explanation
        
        Output "Praise" if the comment:
        - Expresses appreciation or gratitude
        - Shares positive feedback
        - Compliments the content
        - Does not ask a question
        
        IMPORTANT:
        - You must output ONLY "Question" or "Praise" - nothing else
        - If a comment has both praise AND a question, output "Question"
        - Be decisive - choose the primary intent of the comment
        """,
        output_key="comment_type"  # Store type in session state
    )
    
    return router_agent

