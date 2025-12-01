"""
Simple test script to verify the system works correctly.

Run this to test the comment responder with sample comments.
"""

import asyncio
import os
from main import create_root_agent, setup_retry_config
from google.adk.runners import InMemoryRunner


async def test_comment(comment: str):
    """
    Test the system with a sample comment.
    
    Args:
        comment: The comment to test
    """
    print(f"\n{'='*60}")
    print(f"Testing comment: {comment}")
    print(f"{'='*60}\n")
    
    # Setup
    retry_config = setup_retry_config()
    agent = create_root_agent(retry_config)
    runner = InMemoryRunner(agent=agent)
    
    # Process comment
    response = await runner.run_debug(comment)
    
    # Print response
    print("\n--- RESPONSE ---")
    for event in response:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text)
    print("\n")


async def main():
    """Run test cases."""
    # Check API key
    if not os.environ.get("GOOGLE_API_KEY"):
        print("⚠️  ERROR: GOOGLE_API_KEY not set!")
        print("Please set it: export GOOGLE_API_KEY='your-key'")
        return
    
    print("🧪 Testing YouTube Comment Responder System\n")
    
    # Test cases
    test_cases = [
        "Thanks for the video!",  # Should be filtered (simple thanks)
        "Great explanation!",  # Should be filtered (simple praise)
        "What is a good GATE score?",  # Question - should trigger search + transcript
        "Can you explain more about M.Tech placements?",  # Question
        "Love your teaching style!",  # Praise - should get thank you
    ]
    
    for comment in test_cases:
        await test_comment(comment)
        await asyncio.sleep(1)  # Small delay between tests


if __name__ == "__main__":
    asyncio.run(main())

