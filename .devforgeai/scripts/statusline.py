#!/usr/bin/env python3
"""
DevForgeAI StatusLine Script (Universal)
Works on Windows, Linux, macOS, and WSL
"""

import sys
import json
import subprocess
import os
from pathlib import Path

# Fix Unicode encoding on Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def run_command(cmd, check=False):
    """Run shell command and return output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=check
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""

def get_git_branch():
    """Get current git branch if in a repo"""
    # Check if we're in a git repo
    git_check = run_command("git rev-parse --git-dir 2>nul" if os.name == 'nt' else "git rev-parse --git-dir 2>/dev/null")
    if not git_check:
        return ""

    branch = run_command("git branch --show-current 2>nul" if os.name == 'nt' else "git branch --show-current 2>/dev/null")
    return f" | 🌿 {branch}" if branch else ""

def calculate_context(input_data, transcript_path):
    """Calculate context usage with progress bar"""
    model_name = input_data.get('model', {}).get('display_name', 'Claude')

    # Determine context limit based on model
    if '1M' in model_name:
        context_limit = 800000  # 800k usable for 1M Sonnet models
    else:
        context_limit = 160000  # 160k usable for 200k models

    # Extract token usage from transcript
    total_tokens = 0
    if transcript_path and os.path.exists(transcript_path):
        try:
            with open(transcript_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            most_recent_usage = None
            for line in lines:
                try:
                    data = json.loads(line.strip())
                    if not data.get('isSidechain', False) and data.get('message', {}).get('usage'):
                        most_recent_usage = data['message']['usage']
                except:
                    continue

            if most_recent_usage:
                total_tokens = (
                    most_recent_usage.get('input_tokens', 0) +
                    most_recent_usage.get('cache_read_input_tokens', 0) +
                    most_recent_usage.get('cache_creation_input_tokens', 0)
                )
        except:
            total_tokens = 0

    if total_tokens == 0:
        total_tokens = 17900  # Default starting value

    # Calculate progress
    progress_pct = (total_tokens * 100) / context_limit
    progress_pct_int = int(progress_pct)

    # Format tokens
    formatted_tokens = f"{total_tokens // 1000}k"
    formatted_limit = f"{context_limit // 1000}k"

    # Create progress bar
    filled_blocks = min(progress_pct_int // 10, 10)
    empty_blocks = 10 - filled_blocks

    # Color based on usage
    if progress_pct_int < 50:
        bar_color = "\033[38;5;114m"  # Green
    elif progress_pct_int < 80:
        bar_color = "\033[38;5;215m"  # Orange
    else:
        bar_color = "\033[38;5;203m"  # Red

    gray_color = "\033[38;5;242m"
    text_color = "\033[38;5;250m"
    reset = "\033[0m"

    # Build progress bar
    progress_bar = f"{bar_color}{'█' * filled_blocks}{gray_color}{'░' * empty_blocks}{reset} {text_color}{progress_pct:.1f}% ({formatted_tokens}/{formatted_limit}){reset}"

    return progress_bar

def main():
    """Main statusline logic"""
    # Read JSON input from stdin
    try:
        input_data = json.load(sys.stdin)
    except:
        input_data = {}

    # Extract basic info
    cwd = input_data.get('workspace', {}).get('current_dir') or input_data.get('cwd', '')
    model_name = input_data.get('model', {}).get('display_name', 'Claude')
    transcript_path = input_data.get('transcript_path', '')

    # Get git branch
    git_branch = get_git_branch()

    # Calculate context usage
    progress_info = calculate_context(input_data, transcript_path)

    # Build statusline (DevForgeAI format)
    # Line 1: Context progress | Model
    # Line 2: Git branch | Additional info
    print(f"{progress_info} | Model: {model_name}")
    print(f"{git_branch} | DevForgeAI-SDF")

if __name__ == "__main__":
    main()
