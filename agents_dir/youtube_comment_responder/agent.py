"""
Agent definition for ADK web interface.

This file is required for `adk web` to discover and run the agent.
"""

import os
import sys
from pathlib import Path

# Add project root to path so we can import root_agent
# This file is in: agents_dir/youtube_comment_responder/agent.py
# Project root is: agents_dir/../ (two levels up)
# Use absolute path resolution for reliability
if '__file__' in globals():
    current_file = Path(__file__).resolve()
else:
    # Fallback: assume we're in the agent directory
    current_file = Path.cwd().resolve() / "agent.py"
    if not current_file.exists():
        # Try alternative: go up from current directory
        current_file = Path.cwd().resolve()

# Go up two levels: agent.py -> youtube_comment_responder -> agents_dir -> project root
project_root = current_file.parent.parent.parent.resolve()
if not (project_root / "root_agent.py").exists():
    # Try going up one more level if needed
    project_root = current_file.parent.parent.parent.parent.resolve()

sys.path.insert(0, str(project_root))

from google.genai import types
from root_agent import create_root_agent


# Setup retry configuration
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# Create and export the root agent
# ADK web looks for 'root_agent' variable (not 'agent')
root_agent = create_root_agent(retry_config)

