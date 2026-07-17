from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater

from agents.host_agent.agent import HostAgent
# Changed from `a2a.utils` because this SDK version moved the task/message helpers into `a2a.helpers.proto_helpers`.
from a2a.helpers.proto_helpers import new_task_from_user_message, new_text_message

from a2a.types import (
    Task,
    TaskState,
    UnsupportedOperationError
)

import asyncio

class HostAgentExecutor(AgentExecutor):
    """
    Implements the AgentExecutor interface to integrate the 
    host agent with the A2A framework.
    """

    def __init__(self):
        self.agent = HostAgent()

    async def create(self):
        """
        Factory method to create and asynchronously initialize the HostAgentExecutor.
        """
        await self.agent.create()
    
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """
        Executes the agent with the provided context and event queue.
        """
        query = context.get_user_input()
        task = context.current_task
        if not task:
            # Changed from `new_task(context.message)` because the SDK now expects the task to be created from the user message object.
            task = new_task_from_user_message(context.message)
            await event_queue.enqueue_event(task)

        # Changed from `contextId` because the generated protobuf fields now use snake_case (`context_id`).
        updater = TaskUpdater(event_queue, task.id, task.context_id)
        
        try:
            # Kept the same streaming flow, but now it uses the updated helper/message API.
            async for item in self.agent.invoke(query, task.context_id):
                is_task_complete = item.get("is_task_complete", False)

                if not is_task_complete:
                    message = item.get('updates','The Agent is still working on your request.')
                    await updater.update_status(
                        TaskState.TASK_STATE_WORKING,
                        # Changed from `new_agent_text_message` because the SDK now uses `new_text_message`.
                        new_text_message(message, context_id=task.context_id, task_id=task.id)
                    )
                else:
                    final_result = item.get('content','no result received')
                    await updater.update_status(
                        TaskState.TASK_STATE_COMPLETED,
                        # Same change as above: use the current helper while preserving the original completion behavior.
                        new_text_message(final_result, context_id=task.context_id, task_id=task.id)
                    )

                    await asyncio.sleep(0.1)  # Allow time for the message to be processed

                    break
        except Exception as e:
            print(f"[Executor Error] Failed executing task: {e}")
            import traceback
            traceback.print_exc()

            error_message = f"An error occurred: {str(e)[:500]}" 
            
            await updater.update_status(
                TaskState.TASK_STATE_FAILED,
                # Same helper change as above, but for the failure path so errors still reach the task stream.
                new_text_message(error_message, context_id=task.context_id, task_id=task.id)
            )
            raise

    async def cancel(self, request: RequestContext, event_queue: EventQueue) -> Task | None:
        raise UnsupportedOperationError()