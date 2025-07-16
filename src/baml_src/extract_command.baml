class Command{
    command string
}

class ChatResponse{
  query_response string
}

function GenerateChatResponseOpenAI(terminal_history: string, user_input: string) -> ChatResponse{
  client OpenAIClient
  prompt #"
    You are a helpful linux terminal assistant.
    Examine any provided terminal history and the user's request, then output a response to the user's query. Return the response STRICTLY according to the format provided below.

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




function GenerateCommandOpenAI(terminal_history: string, user_input: string) -> Command{
  // see ollama-clients.baml
  client OpenAIClient


  // The prompt uses Jinja syntax. Change the models or this text and watch the prompt preview change!
  prompt #"
    Examine any provided terminal history and the user's request, then output a shell command according to the following schema. You are STRICTYLY FORBIDDEN from returning anything else other than the command that will fulfil the user's request. 

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


function GenerateChatResponseGemeni(terminal_history: string, user_input: string) -> ChatResponse{
  client GeminiClient
  prompt #"
    You are a helpful linux terminal assistant.
    Examine any provided terminal history and the user's request, then output a response to the user's query. Return the response STRICTLY according to the format provided below.

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




function GenerateCommandGemeni(terminal_history: string, user_input: string) -> Command{
  // see ollama-clients.baml
  client GeminiClient


  // The prompt uses Jinja syntax. Change the models or this text and watch the prompt preview change!
  prompt #"
    Examine any provided terminal history and the user's request, then output a shell command according to the following schema. You are STRICTYLY FORBIDDEN from returning anything else other than the command that will fulfil the user's request. 

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

test TestName {
  functions [GenerateCommandOpenAI]
  args {
    terminal_history #"
     
    "#
    user_input #"
      say hello
    "#
  }
}
