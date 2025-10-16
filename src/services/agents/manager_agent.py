from smolagents import CodeAgent, LogLevel
from src.services.agents.ollama_model import ollama_model
import yaml
import os
# Agents
from src.services.agents.web_agent import web_agent
from src.services.agents.description_agent import description_agent
# Tools
from src.services.agents.tools.final_answer import FinalAnswerTool

def manager_agent():
    # Local Model Ollama
    model = ollama_model(temperature=0.2)

    # System prompt YAML
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "manager_system_prompt.yaml")
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_templates = yaml.safe_load(f)

    # Agent
    manager = CodeAgent(
        name="manager_agent",
        description=(
            "Central coordinator agent responsible for managing and orchestrating specialized agents. "
            "It assigns tasks, monitors progress, and integrates outputs from other agents to achieve complex goals."
        ),
        model=model,
        tools=[
            FinalAnswerTool()
        ],
        managed_agents=[
            web_agent(),
            description_agent()
            ],
        additional_authorized_imports=["time", "json"],
        prompt_templates=prompt_templates,
        # verbosity_level=LogLevel.DEBUG,
        verbosity_level=LogLevel.INFO,
        max_steps=2,
        planning_interval=3,
        return_full_result=True,
    )

    return manager
