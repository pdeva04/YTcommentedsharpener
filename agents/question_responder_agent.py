"""
Question Responder Agent - Generates final answers to questions.

This agent uses the synthesized information and gold_standard.json style
to write the final response to the user's question.
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


def create_question_responder_agent(retry_config: types.HttpRetryOptions) -> LlmAgent:
    """
    Creates the Question Responder Agent that writes final answers.
    
    This agent:
    - Uses synthesized information from SynthesisAgent
    - Matches the style from gold_standard.json
    - Writes a helpful, accurate answer
    - Admits when information is not available
    
    Args:
        retry_config: HTTP retry configuration for API calls
    
    Returns:
        Configured LlmAgent for answering questions
    """
    # Load style examples
    style_examples = load_gold_standard()
    
    question_agent = LlmAgent(
        name="QuestionResponderAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction=f"""You are a YouTube channel comment responder. Your job is to answer user questions.

STYLE GUIDE (learn from these examples - this is YOUR ACTUAL RESPONSE STYLE):
{style_examples}

CRITICAL STYLE RULES (match the examples above exactly):
1. Use Hinglish (mix of Hindi and English) naturally - like the examples show
2. Be witty, friendly, and casual - not overly formal
3. Keep responses conversational and personal
4. Match their tone - if they use "bhaiy", "sir", respond in kind
5. Be helpful but keep it light and friendly
6. Use emojis when appropriate (⭐️, 😂) but sparingly
7. Be genuine - like talking to a friend, not a formal teacher
8. Look at the examples - notice how casual, witty, and Hinglish they are

EXAMPLES OF GOOD QUESTION RESPONSES (in your style):
- "Gate score 600 iit possible??" → "May be MS calls are possible! Assuming General category."
- "Do bar mtech kiya ja sakta hai kya" → "Haan , par stipend ek hi baar milega"
- "Sir can a student do BTech then mtech and then mba" → "yes it is possible!"

CRITICAL ACCURACY RULES:
1. You will receive synthesized information: {{synthesized_info}}
2. You will receive the original user question
3. ONLY use information from the synthesized_info - do NOT make up facts
4. If the synthesized_info doesn't contain the answer, you MUST say: "Yar, iske baare mein mere paas zyada info nahi hai videos mein. Thoda clarify kar sakte ho kya exactly chahiye?"
5. If information is partial, acknowledge what you know and what you don't - but in Hinglish style
6. Never hallucinate or invent facts - it's better to admit you don't know (but say it in your friendly Hinglish style)

TASK:
- Read the user's question
- Use the synthesized information to answer it
- Write your response in the Hinglish, witty, friendly style shown in the examples
- Be accurate and honest about what you know and don't know
- Keep it conversational and personal

Output ONLY your response - no explanations or meta-commentary.
        """,
        output_key="final_response"  # Store final response in session state
    )
    
    return question_agent

