from src.services.agents.agent import classipy_agent

class AgentService:
    def __init__(self):
        self.agent = classipy_agent()

    def run(self, prompt: str):
        return self.agent.run(prompt)