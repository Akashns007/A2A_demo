from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.utils import new_agent_text_message
from pydantic import BaseModel
from services.execute_agent import agent_run
import asyncio


class AirbnbAgent(BaseModel):
    query: str
    
    async def invoke(self):
        return await agent_run(self.query)


class AirbnbAgentExecutor(AgentExecutor):
    
    async def execute(self, context: RequestContext, event_queue: EventQueue):
        try:
            # Extract query from the request context
            query = context.message.parts[0].root.text
            
            if not query:
                error_msg = "No query provided in request"
                await event_queue.enqueue_event(new_agent_text_message(error_msg))
                return
            
            # Create and invoke the Airbnb agent
            agent = AirbnbAgent(query=query)
            result = await agent.invoke()
            
            # Send the result back through event queue
            await event_queue.enqueue_event(new_agent_text_message(str(result)))
            
        except Exception as e:
            error_msg = f"Error executing Airbnb agent: {str(e)}"
            print(f"AirbnbAgentExecutor error: {e}")
            await event_queue.enqueue_event(new_agent_text_message(error_msg))

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        # Acknowledge cancellation
        await event_queue.enqueue_event(new_agent_text_message("Airbnb agent execution cancelled"))
