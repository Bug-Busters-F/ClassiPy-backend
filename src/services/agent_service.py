from src.services.agents.manager_agent import manager_agent

class AgentService:
    def __init__(self):
        self.manager_agent = manager_agent()

    def run(self, prompt: str):
        return self.manager_agent.run(prompt)