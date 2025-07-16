from baml_client.sync_client import b
from vity.config import config
from vity import sanitizor
from typing import Optional
import os
import re



def load_configs():
    """Get OpenAI client with proper error handling"""
    api_key = None
    base_url = None
    llm_model = None
    
    # Try to get API key from config first
    if config and hasattr(config, 'vity_llm_api_key'):
        api_key = config.vity_llm_api_key
    if config and hasattr(config, 'vity_llm_base_url'):
        base_url = config.vity_llm_base_url
    if config and hasattr(config, 'vity_llm_model'):
        llm_model = config.vity_llm_model
    
    
    if not api_key:
        raise ValueError("VITY_LLM_API_KEY not found. Please run 'vity config' to set it up. Set VITY_LLM_API_KEY 'NONE' if you don't need an API key. ")
    if not base_url:
        raise ValueError("VITY_LLM_BASE_URL not found. Please run 'vity config' to set it up.")
    if not llm_model:
        raise ValueError("VITY_LLM_MODEL not found. Please run 'vity config' to set it up.")
    
    os.environ['BAML_BASE_URL'] = config.vity_llm_base_url
    os.environ['BAML_MODEL'] = config.vity_llm_model
    os.environ['BAML_LOG'] = 'error'
    if config.vity_llm_api_key and config.vity_llm_api_key != 'NONE':
        os.environ['BAML_API_KEY'] = config.vity_llm_api_key
    else:
        os.environ['BAML_API_KEY'] = ""

    

    


def remove_terminal_history_tags(text: str) -> str:
    """
    Removes anything included inside <terminal_history>...</terminal_history> tags in the given text,
    including the tags themselves.
    """
    return re.sub(r"<terminal_history>.*?</terminal_history>", "", text, flags=re.DOTALL)




def generate_command(terminal_history: Optional[str], chat_history: Optional[list], user_input: str, provider: str = "openai") -> list:
    load_configs()   
    sanitized_history = sanitizor.get_last_x_lines(sanitizor.sanitize_raw_log(terminal_history), config.vity_terminal_history_limit)
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
    

    if provider == "google":
        response = b.GenerateCommandGemeni(sanitized_history, user_input)
    elif provider == "openai":
        response = b.GenerateCommandOpenAI(sanitized_history, user_input)
    else:
        raise ValueError(f"Unknown provider was passed: {provider} ")

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

def generate_chat_response(terminal_history: Optional[str], chat_history: Optional[list], user_input: str, provider: str = "openai") -> list:
    load_configs()   
    sanitized_history = sanitizor.get_last_x_lines(sanitizor.sanitize_raw_log(terminal_history), config.vity_terminal_history_limit)
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
    
    if provider == "google":
        response = b.GenerateChatResponseGemeni(sanitized_history, user_input)
    elif provider == "openai":
        response = b.GenerateChatResponseOpenAI(sanitized_history, user_input)
    else:
        raise ValueError(f"Unknown provider was passed: {provider} ")

    messages.append(
        {
            "role": "assistant",
            "content": [
                {
                    "type": "output_text",
                    "text": f"{response.query_response}"
                }
            ]
        }
    )
    return messages
