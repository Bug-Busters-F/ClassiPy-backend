from src.services.agent_service import AgentService

service = AgentService()
result = service.run("what color is the sky?")
print(result.output)