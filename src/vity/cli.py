#!/usr/bin/env python3
"""
Vity CLI - AI-powered terminal assistant
"""
import sys
import os
import argparse
import json
from pathlib import Path
from typing import Optional

from .config import config
from .llm import generate_command, generate_chat_response, remove_terminal_history_tags
from .schema import Command
from . import __version__


def setup_config() -> bool:
    """Setup configuration on first run"""
    config_dir = Path.home() / ".config" / "vity"
    config_file = config_dir / ".env"
    
    if not config_file.exists():
        print("🤖 Welcome to Vity! Let's set up your OpenAI API key.")
        print("You can get one at: https://platform.openai.com/api-keys")
        print()
        
        api_key = input("Enter your OpenAI API key: ").strip()
        if not api_key:
            print("❌ API key is required")
            return False
        
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file.write_text(f"OPENAI_API_KEY={api_key}\n")
        
        print("✅ Configuration saved!")
        print(f"Config file: {config_file}")
        print()
        
        # Set environment variable for this session
        os.environ["OPENAI_API_KEY"] = api_key
        
    return True


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Vity - AI-powered terminal assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  vity do "find all python files"
  vity chat "explain this error"
  vity -f session.log do "fix the deployment issue"
  vity -c chat.json chat "continue our conversation"
  vity -f session.log -c chat.json do "help with this error"
  vity config --reset
  vity reinstall
  
For shell integration, run: vity install
        """
    )
    
    parser.add_argument(
        "-f", "--file", dest="history_file",
        help="Path to terminal session log file for context"
    )
    parser.add_argument(
        "-c", "--chat", dest="chat_file",
        help="Path to chat history file for conversation context"
    )
    parser.add_argument(
        "-m", "--mode", dest="interaction_mode",
        choices=["do", "chat"],
        default="do",
        help="Interaction mode (default: do)"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Do command
    do_parser = subparsers.add_parser("do", help="Generate shell command")
    do_parser.add_argument("prompt", nargs="+", help="What you want to do")
    
    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Chat with AI")
    chat_parser.add_argument("prompt", nargs="+", help="Your question")
    
    # Install command
    install_parser = subparsers.add_parser("install", help="Install shell integration")
    
    # Reinstall command
    reinstall_parser = subparsers.add_parser("reinstall", help="Reinstall shell integration")
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_parser.add_argument("--reset", action="store_true", help="Reset configuration")
    
    args = parser.parse_args()
    
    # Handle special commands first (always available)
    if args.command == "install":
        install_shell_integration()
        return
    
    if args.command == "reinstall":
        reinstall_shell_integration()
        return
    
    if args.command == "config":
        if args.reset:
            reset_config()
            return
        else:
            show_config()
            return
    
    # Setup config if needed (for other commands)
    if not setup_config():
        sys.exit(1)
    
    # Handle main commands
    if not args.command:
        parser.print_help()
        return
    
    if args.command in ["do", "chat"]:
        user_input = " ".join(args.prompt)
        
        # Load terminal history if provided
        terminal_history = ""
        if args.history_file:
            try:
                with open(args.history_file, "r") as f:
                    terminal_history = f.read()
            except FileNotFoundError:
                print(f"⚠️  Warning: history file '{args.history_file}' not found")
        
        # Load chat history if provided
        chat_history = []
        if args.chat_file:
            try:
                with open(args.chat_file, "r") as f:
                    chat_history = json.load(f)
            except FileNotFoundError:
                # Create empty chat history file if it doesn't exist
                chat_history = []
            except json.JSONDecodeError:
                print(f"⚠️  Warning: chat file '{args.chat_file}' contains invalid JSON, starting fresh")
                chat_history = []
        
        print("🤖 Vity is thinking...")
        
        try:
            if args.command == "do":
                updated_chat_history = generate_command(terminal_history, chat_history, user_input)

                for message in reversed(updated_chat_history):
                    if message["role"] == "user":
                        message["content"][0]["text"] = remove_terminal_history_tags(message["content"][0]["text"]) 
                        break

                # Extract the command from the last assistant message
                last_assistant_msg = None
                for msg in reversed(updated_chat_history):
                    if msg.get("role") == "assistant":
                        last_assistant_msg = msg
                        break
                
                if last_assistant_msg:
                    # Extract command from assistant response
                    content = last_assistant_msg.get("content", [{}])[0].get("text", "")
                    if " # " in content:
                        cmd_part = content.split(" # ")[0]
                        comment_part = content.split(" # ")[1].replace(" * vity generated command", "")
                        cmd_string = f"{cmd_part} # {comment_part}"
                        print(f"Command: {cmd_string}")
                        
                        # Add to bash history
                        history_file = Path.home() / ".bash_history"
                        if history_file.exists():
                            with open(history_file, "a") as f:
                                f.write(f"{cmd_string} # Vity generated\n")
                    else:
                        print(f"Command: {content}")
                
                # Save updated chat history
                if args.chat_file:
                    with open(args.chat_file, "w") as f:
                        json.dump(updated_chat_history, f, indent=2)
                
            elif args.command == "chat":
                updated_chat_history = generate_chat_response(terminal_history, chat_history, user_input)

                for message in reversed(updated_chat_history):
                    if message["role"] == "user":
                        message["content"][0]["text"] = remove_terminal_history_tags(message["content"][0]["text"]) 
                        break

                # Extract the response from the last assistant message
                last_assistant_msg = None
                for msg in reversed(updated_chat_history):
                    if msg.get("role") == "assistant":
                        last_assistant_msg = msg
                        break
                
                if last_assistant_msg:
                    content = last_assistant_msg.get("content", [{}])[0].get("text", "")
                    print(content)
                
                # Save updated chat history
                if args.chat_file:
                    with open(args.chat_file, "w") as f:
                        json.dump(updated_chat_history, f, indent=2)
                
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)


def install_shell_integration():
    """Install shell integration"""
    script_content = '''
# Vity shell integration
vity() {
    if [[ "$1" == "record" ]]; then
        shift
        log_dir="$HOME/.local/share/vity/logs"
        chat_dir="$HOME/.local/share/vity/chat"
        mkdir -p "$log_dir"
        mkdir -p "$chat_dir"
        logfile="$log_dir/$(date +%Y%m%d-%H%M%S)-$$.log"
        chatfile="$chat_dir/$(date +%Y%m%d-%H%M%S)-$$.json"
        
        export VITY_ACTIVE_LOG="$logfile"
        export VITY_ACTIVE_CHAT="$chatfile"
        echo "🔴 Starting recording session"
        echo "📝 Use 'vity do' or 'vity chat' for contextual help"
        echo "🛑 Type 'exit' to stop recording"
        
        script -f "$logfile"
        
        unset VITY_ACTIVE_LOG VITY_ACTIVE_CHAT
        echo "🟢 Recording session ended"
        
    elif [[ "$1" == "do" ]]; then
        shift
        if [[ -n "$VITY_ACTIVE_LOG" && -f "$VITY_ACTIVE_LOG" ]]; then
            command vity -f "$VITY_ACTIVE_LOG" -c "$VITY_ACTIVE_CHAT" do "$@"
        else
            echo "⚠️  No active recording. Use 'vity record' for context."
            command vity do "$@"
        fi
        
    elif [[ "$1" == "chat" ]]; then
        shift
        if [[ -n "$VITY_ACTIVE_LOG" && -f "$VITY_ACTIVE_LOG" ]]; then
            command vity -f "$VITY_ACTIVE_LOG" -c "$VITY_ACTIVE_CHAT" chat "$@"
        else
            echo "⚠️  No active recording. Use 'vity record' for context."
            command vity chat "$@"
        fi
        
    elif [[ "$1" == "status" ]]; then
        if [[ -n "$VITY_ACTIVE_LOG" ]]; then
            echo "🔴 Recording active:"
            echo "  📝 Terminal log: $VITY_ACTIVE_LOG"
            echo "  💬 Chat history: $VITY_ACTIVE_CHAT"
        else
            echo "⚫ No active recording"
        fi
        
    # Forward commands that should be handled directly by the Python CLI
    elif [[ "$1" == "install" || "$1" == "reinstall" || "$1" == "config" ]]; then
        # Call the underlying vity executable with the provided arguments unchanged
        command vity "$@"
        
    elif [[ "$1" == "help" || "$1" == "-h" || "$1" == "--help" ]]; then
        cat << 'EOF'
🤖 Vity - AI Terminal Assistant

USAGE:
    vity <command> [options] [prompt]

COMMANDS:
    do <prompt>      Generate a shell command (adds to history)
    chat <prompt>    Chat with AI about terminal/coding topics
    record           Start recording session for context
    status           Show current recording status
    config           Show configuration
    config --reset   Reset configuration (always available)
    install          Install shell integration (always available)
    reinstall        Reinstall shell integration (always available)
    help             Show this help message

EXAMPLES:
    vity do "find all python files"
    vity chat "explain this error message"
    vity record
    vity do "deploy the app"  # (with context from recording)
    vity status
    vity config --reset
    vity reinstall

CONTEXT:
    • Use 'vity record' to start capturing session context
    • Commands run during recording provide better AI responses
    • Recording captures both terminal output and chat history
    • Recording indicator (🔴) shows in your prompt
    • Use 'exit' to stop recording
EOF
        
    else
        # Show help for unknown commands or no arguments
        if [[ -n "$1" ]]; then
            echo "❌ Unknown command: $1"
            echo ""
        fi
        echo "🤖 Vity - AI Terminal Assistant"
        echo ""
        echo "Usage: vity <command> [prompt]"
        echo ""
        echo "Commands:"
        echo "  do <prompt>      Generate shell command"
        echo "  chat <prompt>    Chat with AI"
        echo "  record           Start recording session"
        echo "  status           Show recording status"
        echo "  config           Show configuration"
        echo "  config --reset   Reset configuration"
        echo "  install          Install shell integration"
        echo "  reinstall        Reinstall shell integration"
        echo "  help             Show detailed help"
        echo ""
        echo "Run 'vity help' for more details and examples."
    fi
    
    history -n 2>/dev/null || true
}
'''
    
    bashrc = Path.home() / ".bashrc"
    if bashrc.exists():
        content = bashrc.read_text()
        if "# Vity shell integration" not in content:
            with open(bashrc, "a") as f:
                f.write(f"\n{script_content}")
            print("✅ Shell integration installed!")
            print("Run 'source ~/.bashrc' or start a new terminal session")
        else:
            print("✅ Shell integration already installed")
    else:
        print("❌ ~/.bashrc not found")


def reinstall_shell_integration():
    """Reinstall shell integration (remove existing and install fresh)"""
    bashrc = Path.home() / ".bashrc"
    
    if not bashrc.exists():
        print("❌ ~/.bashrc not found")
        return
    
    print("🔄 Reinstalling shell integration...")
    
    # Read the current bashrc content
    content = bashrc.read_text()
    
    # Find and remove existing vity shell integration
    lines = content.split('\n')
    new_lines = []
    in_vity_section = False
    
    for line in lines:
        if line.strip() == "# Vity shell integration":
            in_vity_section = True
            print("🗑️  Removing existing shell integration...")
            continue
        elif in_vity_section and line.strip() == "}":
            in_vity_section = False
            continue
        elif not in_vity_section:
            new_lines.append(line)
    
    # Write the cleaned content back
    bashrc.write_text('\n'.join(new_lines))
    
    # Install fresh shell integration
    print("✨ Installing fresh shell integration...")
    install_shell_integration()



def reset_config():
    """Reset configuration"""
    config_dir = Path.home() / ".config" / "vity"
    config_file = config_dir / ".env"
    
    if config_file.exists():
        config_file.unlink()
        print("✅ Configuration reset")
    else:
        print("ℹ️  No configuration found")


def show_config():
    """Show current configuration"""
    config_dir = Path.home() / ".config" / "vity"
    config_file = config_dir / ".env"
    
    if config_file.exists():
        print(f"📁 Config file: {config_file}")
        print("🔑 API key configured")
    else:
        print("❌ No configuration found")
        print("Run 'vity config' to set up")


if __name__ == "__main__":
    main() 