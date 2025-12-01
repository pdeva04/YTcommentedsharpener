"""
Search Agent - Uses Google Search to find information for answering questions.

This agent searches the web for current information that might help answer
the user's question.
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from google.genai import types


def create_search_agent(retry_config: types.HttpRetryOptions) -> LlmAgent:
    """
    Creates the Search Agent that uses Google Search to find information.
    
    This agent will:
    - Use google_search tool to find relevant information
    - Extract key points from search results
    - Present findings in a structured format
    
    Args:
        retry_config: HTTP retry configuration for API calls
    
    Returns:
        Configured LlmAgent with Google Search capability
    """
    search_agent = LlmAgent(
        name="SearchAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""You are a research agent that uses Google Search to find information.

Your job:
1. Use the google_search tool to find relevant information about the user's question
2. Extract the most relevant and useful information from search results
3. Present your findings clearly and concisely
4. Focus on information that directly relates to the question

IMPORTANT:
- Only use information from the search results - don't make things up
- If search results don't contain relevant info, say so clearly
- Cite sources when possible
- Keep findings focused and relevant to the question

Output your findings in a clear, structured format.
        """,
        tools=[google_search],  # Enable Google Search tool
        output_key="search_results"  # Store results in session state
    )
    
    return search_agent

