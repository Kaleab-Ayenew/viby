class Command{
    command string
}

class ChatResponse{
  query_response string
}

function GenerateChatResponse(terminal_history: string, user_input: string) -> ChatResponse{
  client OpenAIClient
  prompt #"
    You are a helpful linux terminal assistant.
    Examine any provided terminal history and the user's request, then output a response to the user's query.

    Terminal History:
    ---
    {{ terminal_history }}
    ---

    User Input:
    ---
    {{ user_input }}
    ---

    {# special macro to print the output instructions. #}
    {{ ctx.output_format }}

    JSON:
  "#
}




function GenerateCommand(terminal_history: string, user_input: string) -> Command{
  // see ollama-clients.baml
  client OpenAIClient


  // The prompt uses Jinja syntax. Change the models or this text and watch the prompt preview change!
  prompt #"
    Examine any provided terminal history and the user's request, then output a shell command according to the following schema.

    Terminal History:
    ---
    {{ terminal_history }}
    ---

    User Input:
    ---
    {{ user_input }}
    ---

    {# special macro to print the output instructions. #}
    {{ ctx.output_format }}

    JSON:
  "#
}


