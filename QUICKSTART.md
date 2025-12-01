# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set Your API Key
```bash
export GOOGLE_API_KEY='your-gemini-api-key-here'
```

Get your key from: https://aistudio.google.com/app/api-keys

### Step 3: Run the System

**Option A: Use ADK Web Interface (Easiest)**
```bash
python main.py
# Then in another terminal:
adk web
```

**Option B: Test with Script**
```bash
python test_system.py
```

## 📝 Example Usage

```python
import asyncio
from main import create_root_agent, setup_retry_config
from google.adk.runners import InMemoryRunner

async def respond():
    retry_config = setup_retry_config()
    agent = create_root_agent(retry_config)
    runner = InMemoryRunner(agent=agent)
    
    # Test with a comment
    response = await runner.run_debug("What is a good GATE score?")
    
    for event in response:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text)

asyncio.run(respond())
```

## ✅ What Happens When You Run It

1. **FilterAgent** checks if comment is worthy
2. **RouterAgent** decides: Question or Praise?
3. **Response Generation**:
   - **Praise** → Thank-you message in your style
   - **Question** → Search + Transcript lookup → Synthesis → Answer

## 🎯 Test Comments

Try these to see different behaviors:

- `"Thanks!"` → Filtered out (too simple)
- `"Great video!"` → Filtered out (no substance)
- `"What is a good GATE score?"` → Full question pipeline
- `"Love your teaching style!"` → Praise response
- `"Can you explain M.Tech placements?"` → Full question pipeline

## 🐛 Troubleshooting

**"GOOGLE_API_KEY not set"**
- Make sure you exported the key: `export GOOGLE_API_KEY='your-key'`
- Or create a `.env` file with: `GOOGLE_API_KEY=your-key`

**"File not found" errors**
- Check that `data/gold_standard.json` exists
- Check that `transcripts/Video transcripts.txt` exists

**Import errors**
- Run: `pip install -r requirements.txt`
- Make sure you're using Python 3.8+

## 📚 Next Steps

- Read `README.md` for full documentation
- Customize agents in `agents/` folder
- Add more examples to `data/gold_standard.json`
- Add more transcripts to `transcripts/Video transcripts.txt`

Happy commenting! 🎉

