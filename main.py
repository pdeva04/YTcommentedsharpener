"""
Main entry point for the YouTube Comment Responder system.

This file initializes the agent system and provides a way to run it
using ADK's web interface or programmatically.
"""

import os
from dotenv import load_dotenv
from google.genai import types
from google.adk.runners import InMemoryRunner
from root_agent import create_root_agent

# Load environment variables from .env file
load_dotenv()


def setup_retry_config() -> types.HttpRetryOptions:
    """
    Configures retry options for API calls.
    
    This handles transient errors like rate limits or temporary service unavailability
    by automatically retrying requests with exponential backoff.
    
    Returns:
        Configured HttpRetryOptions object
    """
    return types.HttpRetryOptions(
        attempts=5,  # Maximum retry attempts
        exp_base=7,  # Delay multiplier for exponential backoff
        initial_delay=1,  # Initial delay before first retry (in seconds)
        http_status_codes=[429, 500, 503, 504]  # Retry on these HTTP errors
    )


def main():
    """
    Main function to initialize and run the comment responder system.
    
    This function:
    1. Checks for API key
    2. Creates the root agent
    3. Creates a runner
    4. Provides instructions for using the system
    """
    # Check if API key is set
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("⚠️  WARNING: GOOGLE_API_KEY environment variable not set!")
        print("Please set it using: export GOOGLE_API_KEY='your-key-here'")
        print("Or create a .env file with: GOOGLE_API_KEY=your-key-here")
        return
    
    print("🚀 Initializing YouTube Comment Responder System...")
    print("=" * 60)
    
    # Setup retry configuration
    retry_config = setup_retry_config()
    
    # Create the root agent (which creates all sub-agents)
    print("📦 Creating agents...")
    root_agent = create_root_agent(retry_config)
    print("✅ All agents created successfully!")
    
    # Create runner
    print("🏃 Creating runner...")
    runner = InMemoryRunner(agent=root_agent)
    print("✅ Runner created!")
    
    print("=" * 60)
    print("\n✅ System ready!")
    print("\nTo use the system, you have two options:\n")
    print("OPTION 1: Use ADK Web Interface")
    print("  Run: adk web")
    print("  Then open the URL shown in your browser")
    print("\nOPTION 2: Use programmatically")
    print("  See the example usage below:\n")
    print("  ```python")
    print("  import asyncio")
    print("  from main import create_root_agent, setup_retry_config")
    print("  from google.adk.runners import InMemoryRunner")
    print("  ")
    print("  async def test():")
    print("      retry_config = setup_retry_config()")
    print("      agent = create_root_agent(retry_config)")
    print("      runner = InMemoryRunner(agent=agent)")
    print("      response = await runner.run_debug('Your comment here')")
    print("  ")
    print("  asyncio.run(test())")
    print("  ```\n")
    
    # Return runner for programmatic use
    return runner


if __name__ == "__main__":
    # When run directly, initialize the system
    runner = main()
    
    # If you want to test immediately, uncomment below:
    # import asyncio
    # async def test():
    #     if runner:
    #         response = await runner.run_debug("What is a good GATE score?")
    #         for event in response:
    #             if event.content and event.content.parts:
    #                 for part in event.content.parts:
    #                     if part.text:
    #                         print(f"\n{part.text}")
    # asyncio.run(test())

