"""
Synthesis Agent - Combines information from Search and Transcript agents.

This agent takes results from both SearchAgent and TranscriptAgent and
synthesizes them into a coherent information base for answering questions.
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types


def create_synthesis_agent(retry_config: types.HttpRetryOptions) -> LlmAgent:
    """
    Creates the Synthesis Agent that combines search and transcript results.
    
    This agent will:
    - Take search_results from SearchAgent
    - Take transcript_results from TranscriptAgent
    - Combine and synthesize the information
    - Identify the most relevant information for answering the question
    - Remove duplicates and contradictions
    
    Args:
        retry_config: HTTP retry configuration for API calls
    
    Returns:
        Configured LlmAgent for synthesizing information
    """
    synthesis_agent = LlmAgent(
        name="SynthesisAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""You are a synthesis agent. Your job is to combine information from multiple sources.

You will receive information from:
1. Search results from Google Search: {search_results}
2. Transcript results from video transcripts: {transcript_results}
3. The original user question

Your task:
1. Combine information from both sources
2. Identify the most relevant and useful information for answering the question
3. Remove duplicates and contradictions
4. Prioritize information from transcripts (channel's own content) when available
5. Use search results to supplement or provide additional context
6. Create a coherent summary of key points needed to answer the question

IMPORTANT:
- Only use information that was actually provided in the sources
- If sources contradict, note the contradiction
- If information is missing, clearly state what is missing
- Focus on information that directly helps answer the user's question
- Don't make up facts - if you don't have the information, say so

Output a clear, structured summary of the synthesized information.
        """,
        output_key="synthesized_info"  # Store synthesized info in session state
    )
    
    return synthesis_agent

