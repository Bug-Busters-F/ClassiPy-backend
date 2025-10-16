from smolagents import CodeAgent, LogLevel, LiteLLMModel
from dotenv import load_dotenv
import yaml
import os
# Tools
from src.services.agents.tools.web_search import DuckDuckGoSearchTool
from src.services.agents.tools.visit_webpage import VisitWebpageTool
from src.services.agents.tools.final_answer import FinalAnswerTool

def classipy_agent():
    # Local Model Ollama
    load_dotenv()
    
    ollama_model = os.getenv("OLLAMA_MODEL")
    ollama_port = os.getenv("OLLAMA_API_PORT")
    model_id = f"ollama_chat/{ollama_model}"
    api_base = f"http://localhost:{ollama_port}"

    model = LiteLLMModel(
        model_id=model_id,
        api_base=api_base,
        max_tokens=12000,
        temperature=0.5,
        timeout=180,
        )

    # System prompt YAML
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "system_prompt.yaml")
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_templates = yaml.safe_load(f)

    # Agent
    agent = CodeAgent(
        name="classipy_agent",
        description=(
            "Agent that searches the web for a part number's technical data, creates a detailed description from the extracted specs, and outputs a JSON with part number, description, and used keywords."
        ),
        model=model,
        tools=[
            DuckDuckGoSearchTool(),
            VisitWebpageTool(),
            FinalAnswerTool(),
        ],
        additional_authorized_imports=["time", "json", "typing"],
        prompt_templates=prompt_templates,
        # verbosity_level=LogLevel.DEBUG,
        verbosity_level=LogLevel.INFO,
        max_steps=3,
        planning_interval=3,
        return_full_result=True,
    )

    return agent