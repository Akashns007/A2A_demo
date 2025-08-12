from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.utils import new_agent_text_message
from pydantic import BaseModel
from services.execute_agent import orchestrator_run
import asyncio


class AdvancedOrchestratorAgent(BaseModel):
    query: str
    
    async def invoke(self):
        return await orchestrator_run(self.query)


class AdvancedOrchestratorAgentExecutor(AgentExecutor):
    
    async def execute(self, context: RequestContext, event_queue: EventQueue):
        try:

            query = context.message.parts[0].root.text
            
            if not query:
                error_msg = "No query provided in request"
                await event_queue.enqueue_event(new_agent_text_message(error_msg))
                return
            
            agent = AdvancedOrchestratorAgent(query=query)
            result = await agent.invoke()

            await event_queue.enqueue_event(new_agent_text_message(str(result)))
            
        except Exception as e:
            error_msg = f"Error executing advanced orchestrator agent: {str(e)}"
            print(f"AdvancedOrchestratorAgentExecutor error: {e}")
            await event_queue.enqueue_event(new_agent_text_message(error_msg))

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        await event_queue.enqueue_event(new_agent_text_message("Advanced orchestrator agent execution cancelled"))
