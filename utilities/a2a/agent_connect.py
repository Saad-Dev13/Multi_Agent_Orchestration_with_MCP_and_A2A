from typing import Any
from uuid import uuid4
from a2a.types import (
    AgentCard, 
    SendMessageRequest,
    Role,
    TaskState
)
from a2a.helpers.proto_helpers import new_text_message
import httpx
from a2a.client import create_client, ClientConfig

class AgentConnector:
    """
    Connects to a remote A2A agent and provides a uniform method to delegate tasks
    """

    def __init__(self, agent_card: AgentCard):
        self.agent_card = agent_card

    async def send_task(self, message: str, session_id: str) -> str:
        """
        Send a task to the agent and return the response text
        
        Args:
            message (str): The message to send to the agent
            session_id (str): The session ID for tracking the task

        Returns:
            str: The response text from the agent
        """

        async with httpx.AsyncClient(timeout=300.0) as httpx_client:
            client_config = ClientConfig(httpx_client=httpx_client)
            
            print(f"[Debug] Creating client for agent '{self.agent_card.name}'...")
            a2a_client = await create_client(
                agent=self.agent_card,
                client_config=client_config,
            )

            # Create message using the standard SDK helper
            message_obj = new_text_message(
                text=message,
                context_id=session_id,
                role=Role.ROLE_USER
            )

            request = SendMessageRequest(
                message=message_obj
            )

            print(f"[Debug] Sending message to agent '{self.agent_card.name}'...")
            agent_response = "No response from agent"
            try:
                response_stream = a2a_client.send_message(
                    request=request
                )
                async for event in response_stream:
                    # Find which fields are populated in the StreamResponse
                    populated_fields = [f for f in ["message", "task", "status_update", "artifact_update"] if event.HasField(f)]
                    print(f"[Debug] Received event with populated fields: {populated_fields}")
                    
                    if event.HasField('message'):
                        parts = [part.text for part in event.message.parts if part.text]
                        if parts:
                            agent_response = "".join(parts)
                            
                    elif event.HasField('task') and event.task.status.HasField('message'):
                        parts = [part.text for part in event.task.status.message.parts if part.text]
                        if parts:
                            agent_response = "".join(parts)
                            
                    elif event.HasField('status_update'):
                        status = event.status_update.status
                        state = status.state
                        has_message = status.HasField('message')
                        try:
                            state_name = TaskState.Name(state)
                        except Exception:
                            state_name = str(state)
                        
                        print(f"[Debug] status_update: state={state} ({state_name}), has_message={has_message}")
                        print(f"[Debug]   TaskState.TASK_STATE_COMPLETED={TaskState.TASK_STATE_COMPLETED}, match={state == TaskState.TASK_STATE_COMPLETED}")

                        if has_message:
                            parts = [part.text for part in status.message.parts if part.text]
                            text = "".join(parts)
                            print(f"[Debug]   message parts text={repr(text)}")
                            if text:
                                print(f" -> [{state_name}] {text}")
                                if state == TaskState.TASK_STATE_COMPLETED:
                                    agent_response = text
                                elif state == TaskState.TASK_STATE_FAILED:
                                    agent_response = f"Task failed: {text}"
                        else:
                            print(f"[Debug]   status has no message field")
                                    
            except Exception as e:
                print(f"[Error] Exception in communication stream:")
                import traceback
                traceback.print_exc()
                return f"Error communicating with agent: {e}"

            return agent_response