from src.services.agent_service import AgentService

service = AgentService()
result = service.run("Part_Number: CL10C330JB8NNNC")
print(result.output)