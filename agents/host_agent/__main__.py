import asyncio
import uvicorn
from fastapi import FastAPI

from a2a.types import AgentSkill, AgentCard, AgentCapabilities, AgentInterface
import click
from a2a.server.request_handlers import DefaultRequestHandler

from agents.host_agent.agent_executor import HostAgentExecutor
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.routes import (
    add_a2a_routes_to_fastapi,
    create_agent_card_routes,
    create_jsonrpc_routes,
    create_rest_routes,
)

@click.command()
@click.option('--host', default='localhost', help='Host for the agent server')
@click.option('--port', default=10001, help='Port for the agent server')
def main(host: str, port: int):
    """
    Main function to create and run the Host agent.
    """
    async def serve():
        # CHANGED: Added 'input_modes' and 'output_modes' to comply with updated a2a_pb2.pyi requirements
        skill = AgentSkill(
            id="host_agent_skill",
            name="host_agent_skill",
            description="A simple orchestrator for orchestrating tasks with A2A agents and MCP Tools",
            tags=["host", "orchestrator"],
            examples=[
                """Create a simple webpage with a header and a footer using other agents/tools.""",
            ],
            input_modes=["text"],   # Added
            output_modes=["text"]   # Added
        )

        # CHANGED: Replaced 'url' property with 'supported_interfaces' containing 'AgentInterface' object
        # CHANGED: Updated snake_case properties: 'default_input_modes' and 'default_output_modes'
        agent_card = AgentCard(
            name ="host_agent",
            description="A simple orchestrator for orchestrating tasks",
            supported_interfaces=[
                AgentInterface(
                    url=f"http://{host}:{port}/",
                    protocol_binding="JSONRPC",
                )
            ],
            version="1.0.0",
            default_input_modes=["text"],
            default_output_modes=["text"],
            skills=[skill],
            capabilities=AgentCapabilities(streaming=True),
        )

        # Create agent executor
        agent_executor = HostAgentExecutor()
        await agent_executor.create()

        # CHANGED: Passed 'agent_card' to DefaultRequestHandler to comply with new routing patterns
        request_handler = DefaultRequestHandler(
            agent_executor=agent_executor,
            task_store=InMemoryTaskStore(),
            agent_card=agent_card,
        )

        # CHANGED: Created a clean FastAPI app instance and mounted modern A2A routing engines
        app = FastAPI()
        add_a2a_routes_to_fastapi(
            app,
            agent_card_routes=create_agent_card_routes(agent_card),
            jsonrpc_routes=create_jsonrpc_routes(request_handler, rpc_url='/'),
            rest_routes=create_rest_routes(request_handler),
        )

        # CHANGED: Use uvicorn.Config on the FastAPI app instance instead of the old Starlette wrap
        config = uvicorn.Config(app, host=host, port=port)
        server_instance = uvicorn.Server(config)
        
        await server_instance.serve()

    asyncio.run(serve())


if __name__ == "__main__":
    main()