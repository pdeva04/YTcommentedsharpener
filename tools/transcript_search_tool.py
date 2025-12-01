"""
Custom tool for searching video transcripts.

This tool allows agents to search through video transcripts for relevant information
about topics mentioned in user comments.
"""

import os
from typing import Dict
from google.adk.tools import FunctionTool, ToolContext


def search_transcripts(query: str, tool_context: ToolContext = None) -> Dict:
    """
    Searches through video transcripts for information related to the query.
    
    This function reads the transcripts file and searches for relevant sections
    that contain keywords from the query. It returns matching excerpts with context.
    
    Args:
        query: The search query (keywords or topic to search for)
        tool_context: ADK tool context (automatically provided by ADK)
    
    Returns:
        Dictionary with status and search results:
        Success: {
            "status": "success",
            "matches": [list of matching text excerpts],
            "count": number of matches
        }
        Error: {
            "status": "error",
            "error_message": "description of error"
        }
    """
    try:
        # Get the path to the transcripts file
        # Assuming the file is in transcripts/Video transcripts.txt relative to project root
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        transcripts_path = os.path.join(current_dir, "transcripts", "Video transcripts.txt")
        
        # Check if file exists
        if not os.path.exists(transcripts_path):
            return {
                "status": "error",
                "error_message": f"Transcripts file not found at {transcripts_path}"
            }
        
        # Read the transcripts file
        with open(transcripts_path, "r", encoding="utf-8") as f:
            transcript_content = f.read()
        
        # Convert query to lowercase for case-insensitive search
        query_lower = query.lower()
        query_words = query_lower.split()
        
        # Split transcript into sentences/paragraphs for better matching
        # We'll search for paragraphs that contain any of the query words
        paragraphs = transcript_content.split("\n\n")
        
        matches = []
        for para in paragraphs:
            para_lower = para.lower()
            # Check if paragraph contains any query words
            if any(word in para_lower for word in query_words if len(word) > 2):  # Ignore very short words
                # Take first 500 characters of the paragraph to avoid too long responses
                excerpt = para[:500] + "..." if len(para) > 500 else para
                matches.append(excerpt.strip())
        
        # Limit to top 5 matches to avoid overwhelming the agent
        matches = matches[:5]
        
        if matches:
            return {
                "status": "success",
                "matches": matches,
                "count": len(matches),
                "message": f"Found {len(matches)} relevant section(s) in transcripts"
            }
        else:
            return {
                "status": "success",
                "matches": [],
                "count": 0,
                "message": "No relevant information found in transcripts for this query"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error searching transcripts: {str(e)}"
        }


# Create the FunctionTool wrapper for ADK
transcript_search_tool = FunctionTool(func=search_transcripts)

