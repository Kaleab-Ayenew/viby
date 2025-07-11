client<llm> OpenAIClient {
  provider openai-generic
  options {
    base_url env.BAML_BASE_URL
    model env.BAML_MODEL
    api_key env.BAML_API_KEY
  }
}
