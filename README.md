# YouTube Comment Responder System

A multi-agent system built with Google ADK that automatically responds to YouTube comments in your personal style.

## 🎯 Overview

This system uses specialized AI agents to:
1. **Filter** comments (reject spam/rude comments)
2. **Route** comments (categorize as Question or Praise)
3. **Respond** appropriately:
   - **Praise**: Generate thank-you messages
   - **Questions**: Search transcripts + web, synthesize info, and answer

## 📁 Project Structure

```
YouTube comments/
├── agents/                      # All specialized agents
│   ├── filter_agent.py         # Filters spam/rude comments
│   ├── router_agent.py         # Routes to Question/Praise
│   ├── praise_responder_agent.py  # Handles praise comments
│   ├── search_agent.py          # Google Search for questions
│   ├── transcript_agent.py     # Searches video transcripts
│   ├── synthesis_agent.py      # Combines search + transcript results
│   └── question_responder_agent.py  # Generates final answers
├── tools/                       # Custom tools
│   └── transcript_search_tool.py  # Tool to search transcripts
├── data/                        # Data files
│   └── gold_standard.json      # Your response style examples
├── transcripts/                 # Video transcripts
│   └── Video transcripts.txt   # Your video transcripts
├── root_agent.py               # Main coordinator agent
├── main.py                     # Entry point
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Key

Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/api-keys).

Then set it as an environment variable:

```bash
export GOOGLE_API_KEY='your-api-key-here'
```

Or create a `.env` file:
```
GOOGLE_API_KEY=your-api-key-here
```

### 3. Verify Data Files

Make sure you have:
- `data/gold_standard.json` - Your response style examples
- `transcripts/Video transcripts.txt` - Your video transcripts

## 💻 Usage

### Option 1: ADK Web Interface (Recommended)

```bash
# Start the web server
adk web

# Or if you want to specify the agent
python main.py
adk web
```

Then open the URL shown in your browser to interact with the agent.

### Option 2: Programmatic Usage

```python
import asyncio
from main import create_root_agent, setup_retry_config
from google.adk.runners import InMemoryRunner

async def respond_to_comment():
    # Setup
    retry_config = setup_retry_config()
    agent = create_root_agent(retry_config)
    runner = InMemoryRunner(agent=agent)
    
    # Process a comment
    comment = "What is a good GATE score?"
    response = await runner.run_debug(comment)
    
    # Print response
    for event in response:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text)

asyncio.run(respond_to_comment())
```

## 🔄 How It Works

### Workflow

1. **FilterAgent**: Checks if comment is worthy
   - Rejects: spam, rude comments, simple "thanks"
   - Accepts: meaningful questions or praise

2. **RouterAgent**: Categorizes accepted comments
   - "Question": Needs information/answer
   - "Praise": Needs acknowledgment

3. **Response Generation**:
   - **Praise**: `PraiseResponderAgent` generates thank-you using your style
   - **Question**: 
     - `SearchAgent` + `TranscriptAgent` run in parallel
     - `SynthesisAgent` combines their results
     - `QuestionResponderAgent` writes final answer

### Key Features

- **Style Matching**: Learns from `gold_standard.json` to match your response style
- **Transcript Search**: Searches your own video transcripts for answers
- **Web Search**: Uses Google Search for additional information
- **No Hallucination**: Strictly instructed to only use provided information
- **Parallel Processing**: Search and transcript lookup happen simultaneously for speed

## 🛠️ Customization

### Update Response Style

Edit `data/gold_standard.json` to add more examples of your response style.

### Add More Transcripts

Add more video transcripts to `transcripts/Video transcripts.txt`.

### Modify Filter Rules

Edit `agents/filter_agent.py` to change what comments are filtered out.

## 📝 Notes

- The system uses `gemini-2.5-flash-lite` model for fast responses
- All agents have retry logic for handling API errors
- The system is designed to be honest - it will admit when it doesn't know something
- Responses match your style from `gold_standard.json`

## 🐛 Troubleshooting

### API Key Issues
- Make sure `GOOGLE_API_KEY` is set correctly
- Check that the key is valid and has quota remaining

### File Not Found Errors
- Verify that `data/gold_standard.json` and `transcripts/Video transcripts.txt` exist
- Check file paths in the code match your directory structure

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using Python 3.8+

## 📚 Learn More

- [ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Agents Guide](https://google.github.io/adk-docs/agents/)
- [ADK Tools Guide](https://google.github.io/adk-docs/tools/)

## 🎉 Ready to Use!

Run `python main.py` and then `adk web` to start responding to comments!

