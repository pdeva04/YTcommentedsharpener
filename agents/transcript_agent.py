"""
Transcript Agent - Searches video transcripts for relevant information.

This agent uses a custom tool to search through the channel's video transcripts
to find information that might help answer questions.
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from tools.transcript_search_tool import transcript_search_tool


def create_transcript_agent(retry_config: types.HttpRetryOptions) -> LlmAgent:
    """
    Creates the Transcript Agent that searches video transcripts.
    
    This agent will:
    - Use the transcript_search_tool to find relevant sections
    - Extract information from the channel's own videos
    - Present findings from transcripts
    
    Args:
        retry_config: HTTP retry configuration for API calls
    
    Returns:
        Configured LlmAgent with transcript search capability
    """
    transcript_agent = LlmAgent(
        name="TranscriptAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""You are a transcript search agent. Your job is to search through video transcripts to find relevant information.

Your job:
1. Use the search_transcripts tool to search for information related to the user's question
2. Extract relevant information from the transcript matches
3. Present findings clearly, focusing on what was actually said in the videos
4. If multiple matches are found, prioritize the most relevant ones

IMPORTANT:
- Only use information from the transcript search results - don't make things up
- If no relevant information is found in transcripts, say so clearly
- Quote or paraphrase what was said in the videos accurately
- Keep findings focused on answering the user's question

Output your findings in a clear format, indicating they came from video transcripts.
        """,
        tools=[transcript_search_tool],  # Use custom transcript search tool
        output_key="transcript_results"  # Store results in session state
    )
    
    return transcript_agent

