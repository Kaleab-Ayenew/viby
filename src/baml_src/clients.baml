client<llm> OpenAIClient {
  provider openai-generic
  options {
    api_key env.BAML_API_KEY
    base_url env.BAML_BASE_URL
    model env.BAML_MODEL
  }
}
client<llm> GeminiClient{
  provider google-ai
  options {
    api_key env.BAML_API_KEY
    model env.BAML_MODEL
  }
}