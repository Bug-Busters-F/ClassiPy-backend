from smolagents import LiteLLMModel
from dotenv import load_dotenv
import os

def ollama_model(max_tokens=12000, temperature=0.7, timeout=180) -> LiteLLMModel:
    load_dotenv()

    ollama_model = os.getenv("OLLAMA_MODEL")
    ollama_port = os.getenv("OLLAMA_API_PORT")
    api_base = f"http://localhost:{ollama_port}"

    model = LiteLLMModel(
        model_id=f"ollama_chat/{ollama_model}",
        api_base=api_base,
        max_tokens=max_tokens,
        temperature=temperature,
        timeout=timeout,
    )

    return model