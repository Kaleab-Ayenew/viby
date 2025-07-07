from openai import OpenAI
from baml_client.sync_client import b
from baml_client.types import Command as BamlCommand
from .config import config
from .schema import Command
from . import prompts
from typing import Optional
import os
import re

def remove_terminal_history_tags(text: str) -> str:
    """
    Removes anything included inside <terminal_history>...</terminal_history> tags in the given text,
    including the tags themselves.
    """
    return re.sub(r"<terminal_history>.*?</terminal_history>", "", text, flags=re.DOTALL)


def get_client():
    """Get OpenAI client with proper error handling"""
    api_key = None
    
    # Try to get API key from config first
    if config and hasattr(config, 'openai_api_key'):
        api_key = config.openai_api_key
    
    # Fallback to environment variable
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        raise ValueError("OpenAI API key not found. Please run 'vity config' to set it up.")
    
    return OpenAI(api_key=api_key)

def generate_with_local_llm(terminal_history: Optional[str], chat_history: Optional[list], user_input: str) -> list:
    messages = []
    if chat_history:
        messages.extend(chat_history)
    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": f"{user_input}"
                }
            ]
        }
    )
    

    response = b.GenerateCommand(terminal_history, user_input)

    messages.append(
        {
            "role": "assistant",
            "content": [
                {
                    "type": "output_text",
                    "text": f"{response.command}"
                }
            ]
        }
    )
    return messages

def generate_command(terminal_history: Optional[str], chat_history: Optional[list], user_input: str) -> list:
    client = get_client()

    user_prompt = []
    if terminal_history:
        user_prompt.append(f"<terminal_history>{terminal_history}</terminal_history>")
    user_prompt.append(f"<user_request>{user_input}</user_request>")
    
    
    # Build OpenAI message list dynamically
    messages = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompts.COMMAND_SYSTEM_PROMPT
                    }
                ]
            }
        ]

    # Only add terminal history if we have it
    if chat_history:
        messages.extend(chat_history)

    # Always add the user's query
    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "\n\n".join(user_prompt)
                }
            ]
        }
    )
    response = client.responses.parse(
        model="gpt-4.1-mini",
        input=messages,  # {{ Use the dynamic messages instead of hardcoded array }}
        text_format=Command,
        temperature=0,
        max_output_tokens=2048,
        top_p=1,
        store=True
    )


    messages.append(
        {
            "role": "assistant",
            "content": [
                {
                    "type": "output_text",
                    "text": f"{response.output_parsed.command} # {response.output_parsed.comment} * vity generated command"
                }
            ]
        }
    )


    return messages[1:]

def generate_chat_response(terminal_history: Optional[str], chat_history: Optional[list], user_input: str) -> list:
    client = get_client()
    
    messages = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompts.CHAT_SYSTEM_PROMPT
                    }
                ]
            }
        ]
    
    user_prompt = []
    if terminal_history:
        user_prompt.append(f"<terminal_history>{terminal_history}</terminal_history>")
    user_prompt.append(f"<user_request>{user_input}</user_request>")

    # Only add terminal history if we have it
    if chat_history:
        messages.extend(chat_history)

    # Always add the user's query
    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "\n\n".join(user_prompt)
                }
            ]
        }
    )

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=messages,
        temperature=0,
        max_output_tokens=2048,
        top_p=1,
    )
    messages.append(
        {
            "role": "assistant",
            "content": [
                {
                    "type": "output_text",
                    "text": response.output_text
                }
            ]
        }
    )


    return messages[1:]