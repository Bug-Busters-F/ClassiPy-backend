from smolagents import CodeAgent, LogLevel
from src.services.agents.ollama_model import ollama_model
import yaml
import os
from typing import Any, Dict

def description_agent():
    # Local Model Ollama
    model = ollama_model()

    # System prompt YAML
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "manager_system_prompt.yaml")
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_templates = yaml.safe_load(f)

    # Agent
    description_agent = CodeAgent(
        name="description_agent",
        description=(
                "Agent responsible for converting technical product data into clear and structured descriptions. "
                "It interprets specifications and presents them in a user-friendly format."
        ),
        model=model,
        tools=[],
        additional_authorized_imports=["json", "typing"],
        prompt_templates=prompt_templates,
        # verbosity_level=LogLevel.DEBUG,
        verbosity_level=LogLevel.INFO,
        max_steps=2,
        planning_interval=3,
        return_full_result=True,
    )

    return description_agent
