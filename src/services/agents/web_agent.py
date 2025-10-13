from smolagents import CodeAgent, LogLevel
from src.services.agents.ollama_model import ollama_model
import yaml
import os
# Tools
from src.services.agents.tools.web_search import DuckDuckGoSearchTool
from src.services.agents.tools.visit_webpage import VisitWebpageTool

def web_agent():
    # Local Model Ollama
    model = ollama_model()

    # System prompt YAML
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "manager_system_prompt.yaml")
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_templates = yaml.safe_load(f)

    # Agent
    web_agent = CodeAgent(
        name="web_agent",
        description=(
                "Specialized agent for online information retrieval. "
                "It performs web searches, accesses web pages, and collects data for further analysis."
        ),
        model=model,
        tools=[
            DuckDuckGoSearchTool(),
            VisitWebpageTool()
        ],
        additional_authorized_imports=[
            
        ],
        prompt_templates=prompt_templates,
        # verbosity_level=LogLevel.DEBUG,
        verbosity_level=LogLevel.INFO,
        max_steps=6,
        planning_interval=3,
        return_full_result=True,
    )

    return web_agent
