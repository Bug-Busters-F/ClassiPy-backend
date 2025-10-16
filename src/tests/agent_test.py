from src.services.agent_service import AgentService

service = AgentService()
result = service.run("CL10C330JB8NNNC")
print(result.output)