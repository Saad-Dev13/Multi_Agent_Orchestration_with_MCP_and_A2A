import uvicorn
# Changed from the old `A2AStarletteApplication` import because this SDK version exposes route mounting through FastAPI instead.
from fastapi import FastAPI

from a2a.types import AgentSkill, AgentCard, AgentCapabilities, AgentInterface
import click
from a2a.server.request_handlers import DefaultRequestHandler

from agents.website_builder_simple.agent_executor import WebsiteBuilderSimpleAgentExecutor
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.routes import (
    add_a2a_routes_to_fastapi,
    create_agent_card_routes,
    create_jsonrpc_routes,
    create_rest_routes,
)

@click.command()
@click.option('--host', default='localhost', help='Host for the agent server')
@click.option('--port', default=10000, help='Port for the agent server')
def main(host: str, port: int):
    """
    Main function to create and run the website builder agent.
    """
    # Changed from the older skill setup because this SDK version requires explicit input and output modes.
    skill = AgentSkill(
        id="website_builder_simple_skill",
        name="website_builder_simple_skill",
        description="A simple website builder agent that can create basic web pages",
        tags=["website", "builder", "html", "css", "javascript"],
        examples=[
            """Create a simple webpage with a header and a footer.""",
            """Create a landing page for a product with a call to action button.""",
        ],
        input_modes=["text"],   # Added to comply with new schema
        output_modes=["text"]   # Added to comply with new schema
    )

    agent_card = AgentCard(
        name ="website_builder_simple",
        description="A simple website builder agent that can create basic web pages and is built using google's agent development framework.",
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

    request_handler = DefaultRequestHandler(
        agent_executor=WebsiteBuilderSimpleAgentExecutor(),
        task_store=InMemoryTaskStore(),
        agent_card=agent_card,
    )

    # Changed from the old wrapper-based startup so the app can mount the current A2A routes directly.
    app = FastAPI()
    add_a2a_routes_to_fastapi(
        app,
        agent_card_routes=create_agent_card_routes(agent_card),
        jsonrpc_routes=create_jsonrpc_routes(request_handler, rpc_url='/'),
        rest_routes=create_rest_routes(request_handler),
    )

    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()