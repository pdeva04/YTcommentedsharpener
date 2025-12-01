"""
Root Coordinator Agent - Orchestrates the entire comment response workflow.

This agent coordinates all the specialized agents to process a comment
and generate an appropriate response.
"""

from google.adk.agents import Agent, SequentialAgent, ParallelAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool
from google.genai import types

# Import all the agents
from agents.filter_agent import create_filter_agent
from agents.router_agent import create_router_agent
from agents.praise_responder_agent import create_praise_responder_agent
from agents.search_agent import create_search_agent
from agents.transcript_agent import create_transcript_agent
from agents.synthesis_agent import create_synthesis_agent
from agents.question_responder_agent import create_question_responder_agent


def create_root_agent(retry_config: types.HttpRetryOptions) -> Agent:
    """
    Creates the root coordinator agent that orchestrates the entire workflow.
    
    Workflow:
    1. FilterAgent checks if comment is worthy (outputs "IGNORE" or "ACCEPT")
    2. If ACCEPT, RouterAgent categorizes as "Question" or "Praise"
    3. If "Praise" → PraiseResponderAgent generates thank-you response
    4. If "Question" → Parallel execution:
       - SearchAgent searches Google
       - TranscriptAgent searches transcripts
       Then → SynthesisAgent combines results
       Then → QuestionResponderAgent writes final answer
    
    Args:
        retry_config: HTTP retry configuration for API calls
    
    Returns:
        Configured root Agent that coordinates the workflow
    """
    # Create all specialized agents
    filter_agent = create_filter_agent(retry_config)
    router_agent = create_router_agent(retry_config)
    praise_agent = create_praise_responder_agent(retry_config)
    search_agent = create_search_agent(retry_config)
    transcript_agent = create_transcript_agent(retry_config)
    synthesis_agent = create_synthesis_agent(retry_config)
    question_agent = create_question_responder_agent(retry_config)
    
    # Create parallel agent for search + transcript (runs simultaneously)
    parallel_research = ParallelAgent(
        name="ParallelResearch",
        sub_agents=[search_agent, transcript_agent]
    )
    
    # Create sequential pipeline for question handling
    # Step 1: Run search and transcript in parallel
    # Step 2: Synthesize the results
    # Step 3: Generate final answer
    question_pipeline = SequentialAgent(
        name="QuestionPipeline",
        sub_agents=[parallel_research, synthesis_agent, question_agent]
    )
    
    # Root agent uses LLM to coordinate the workflow
    # It decides which path to take based on filter and router decisions
    root_agent = Agent(
        name="CommentResponderCoordinator",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""You are the coordinator for a YouTube comment response system.

WORKFLOW:
1. First, you MUST call FilterAgent to check if the comment is worthy
   - If FilterAgent outputs "IGNORE", respond with: "This comment doesn't need a response."
   - If FilterAgent outputs "ACCEPT", continue to step 2

2. Call RouterAgent to categorize the comment
   - RouterAgent will output "Question" or "Praise"

3. Based on RouterAgent's output:
   - If "Praise": You MUST call PraiseResponderAgent to generate a thank-you response in Hinglish style
   - If "Question": 
     a. Call QuestionPipeline (which runs SearchAgent and TranscriptAgent in parallel,
        then SynthesisAgent, then QuestionResponderAgent)
     b. The QuestionPipeline will handle everything automatically

4. CRITICAL: Output the response EXACTLY as received - copy it word-for-word

ABSOLUTE RULES FOR RESPONSE HANDLING:
- When PraiseResponderAgent or QuestionPipeline returns a response, you MUST copy it EXACTLY
- DO NOT add any text before or after the response
- DO NOT reformat, summarize, translate, or rewrite
- DO NOT convert Hinglish to English
- DO NOT make it more formal
- DO NOT add explanations like "Based on the information..." or "Here's the answer..."
- Just output the response text exactly as you received it

EXAMPLE:
If QuestionPipeline returns: "Official 2025 cutoffs toh abhi release nahi hue hain, par general category ke liye around 750-780 score chahiye hota hai..."
You MUST output EXACTLY: "Official 2025 cutoffs toh abhi release nahi hue hain, par general category ke liye around 750-780 score chahiye hota hai..."
DO NOT output: "The GATE cutoff for IIT Bombay..." (this is wrong - you reformatted it)

Your ONLY job is to call the right agents and pass through their responses unchanged.
        """,
        tools=[
            AgentTool(agent=filter_agent),
            AgentTool(agent=router_agent),
            AgentTool(agent=praise_agent),
            AgentTool(agent=question_pipeline)  # The entire question pipeline as one tool
        ]
    )
    
    return root_agent

