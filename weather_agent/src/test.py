import asyncio
import httpx
from uuid import uuid4
from a2a.client import A2AClient
from a2a.types import SendMessageRequest, MessageSendParams

async def test_weather_agent():
    query = "What is the weather like on September 15?"
    
    async with httpx.AsyncClient(timeout=120.0) as httpx_client:
        client = A2AClient(url="http://localhost:7001", httpx_client=httpx_client)
        
        send_message_payload = {
            'message': {
                'role': 'user',
                'parts': [{'type': 'text', 'text': query}],
                'messageId': uuid4().hex,
            },
            'sessionId': uuid4().hex
        }
        
        request = SendMessageRequest(id=str(uuid4()), params=MessageSendParams(**send_message_payload))
        response = await client.send_message(request)
        response_data = response.model_dump(mode='json', exclude_none=True)
        
        print(f"Response: {response_data}")

asyncio.run(test_weather_agent())