client<llm> Gemma3n {
  // See https://docs.boundaryml.com/docs/snippets/clients/providers/ollama
  // to learn more about how to configure this client
  //
  // Note that you should run ollama using `OLLAMA_ORIGINS='*' ollama serve`
  // and you'll also need to `ollama pull gemma2` to use this client
  provider ollama
  options {
    base_url "http://localhost:11434/v1"
    model "gemma3n:e2b"
  }
}

