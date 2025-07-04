from openai import OpenAI
import json
import os
from config import config
import sys
import argparse  # {{ Add this import }}
from schema import Command
from llm import generate_command, generate_chat_response

if __name__ == "__main__":
    # {{ Replace the hardcoded file loading and argument parsing with: }}
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="vity terminal assistant")
    parser.add_argument(
        "-f", "--file", dest="history_file",
        help="Path to a terminal-session log file to prime the assistant"
    )
    parser.add_argument(
        "-m", "--mode", dest="interaction_mode",
        help="Mode of interaction with the assistant",
        choices=["chat", "do"],
        default="do"
    )
    parser.add_argument("prompt", nargs=argparse.REMAINDER,
                        help="User prompt for the assistant")
    args = parser.parse_args()

    user_input = " ".join(args.prompt).strip()

    # Load terminal history if requested
    terminal_history = ""
    if args.history_file:
        try:
            with open(args.history_file, "r") as f:
                terminal_history = f.read()
        except FileNotFoundError:
            sys.stderr.write(
                f"[vity] Warning: history file '{args.history_file}' not found; "
                "continuing without it.\n"
            )

    print("vity is thinking...")
    if args.interaction_mode == "do":
        command = generate_command(terminal_history, user_input)
        cmd_string = f"{command.command} # {command.comment} * vity generated command"
        # Append command to bash history file
        with open(os.path.expanduser("~/.bash_history"), "a") as f:
            f.write(cmd_string + "\n")
    elif args.interaction_mode == "chat":
        response = generate_chat_response(terminal_history, user_input)
        print(response)