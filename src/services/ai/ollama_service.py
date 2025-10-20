import os
import ollama
import yaml
import json
import re
from dotenv import load_dotenv

load_dotenv()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

PROMPT_DIR = os.path.join(os.path.dirname(__file__), "prompts")

def load_prompt(prompt_name: str) -> str:
    """Carrega o conteúdo de um prompt YAML"""
    path = os.path.join(PROMPT_DIR, f"{prompt_name}.yaml")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt '{prompt_name}' não encontrado.")
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["instruction"]

def run_ollama(prompt_name: str, text: str) -> dict:
    """
    Executa um prompt do Ollama e retorna JSON decodificado.
    """
    base_prompt = load_prompt(prompt_name)
    full_prompt = f"{base_prompt}\n\nText:\n{text.strip()}"

    try:
        result = ollama.generate(model=OLLAMA_MODEL, prompt=full_prompt)
        raw_output = result["response"]
    except Exception as e:
        return {"error": f"Erro ao executar o modelo: {e}"}

    # Extrai JSON do texto retornado
    match = re.search(r"\{[\s\S]*?\}", raw_output)
    if not match:
        return {"error": "JSON não encontrado", "raw_output": raw_output}

    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return {"error": "Falha ao decodificar JSON", "raw_output": raw_output}