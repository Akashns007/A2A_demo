import httpx  
import asyncio  
from a2a.client import A2AClient  
from a2a.types import SendMessageRequest, MessageSendParams  
from uuid import uuid4
from typing import Dict, Any
from agents import function_tool
import uuid
from services.agent_discovery import AgentDiscoveryService

@function_tool
async def call_agent(agent_name: str, message: str) -> str:
    """
    Tool to call a specific A2A agent with a message
    
    Args:
        agent_name: Name of the agent to call (e.g., "WeatherAgent", "AirbnbAgent")
        message: Message to send to the agent
    
    Returns:
        Response from the agent
    """
    try:

        discovery = AgentDiscoveryService()
        agent_cards = await discovery.discover_agents()

        if agent_name not in agent_cards:
            available_agents = list(agent_cards.keys())
            return f"Agent '{agent_name}' not found. Available agents: {', '.join(available_agents)}"
        
        agent_card = agent_cards[agent_name]
        agent_url = agent_card.url
        
        print(f"Calling {agent_name} at {agent_url} with message: {message[:100]}...")
        
        send_message_payload = {  
            'message': {  
                'role': 'user',  
                'parts': [{'type': 'text', 'text': message}],  
                'messageId': uuid4().hex,  
            },
            'sessionId': uuid4().hex 
        }  
        
        async with httpx.AsyncClient(timeout=60.0) as httpx_client:  
            try:

                client = A2AClient(url=agent_url, httpx_client=httpx_client)
                

                request = SendMessageRequest(
                    id=str(uuid4()),
                    params=MessageSendParams(**send_message_payload)
                )
                response = await client.send_message(request)
                
                response_data = response.model_dump(mode='json', exclude_none=True)
                
                # Extract response text
                if 'message' in response_data and 'parts' in response_data['message']:
                    parts = response_data['message']['parts']
                    if parts and len(parts) > 0 and 'text' in parts[0]:
                        return parts[0]['text']

                return str(response_data)
                
            except Exception as e:
                return f"Error calling {agent_name}: {str(e)}"
                
    except Exception as e:
        print(f"Error in call_agent tool: {e}")
        return f"Failed to call agent {agent_name}: {str(e)}"