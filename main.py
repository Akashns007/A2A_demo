import httpx
from a2a.client import A2AClient
from a2a.types import SendMessageRequest, MessageSendParams
from uuid import uuid4
import json
from datetime import datetime
from typing import Optional
import asyncio
import uuid



class InteractiveA2ATestClient:
    """Interactive test client for A2A orchestrator"""
    
    def __init__(self, orchestrator_url: str = "http://localhost:7000"):
        self.orchestrator_url = orchestrator_url
        self.session_id = uuid4().hex
        self.conversation_history = []
        self.client = None
        self.httpx_client = None
    
    async def __aenter__(self):
        self.httpx_client = httpx.AsyncClient(timeout=120.0)
        try:
            self.client = A2AClient( 
                    url=self.orchestrator_url,
                    httpx_client=self.httpx_client
                )
            return self
        except Exception as e:
            print(f"❌ Failed to connect to orchestrator: {e}")
            raise
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.httpx_client:
            await self.httpx_client.close()
    
    async def send_message(self, message: str) -> str:
        """Send a message to the orchestrator and get response"""
        try:
            print(f"\n📤 Sending: {message}")
            print("⏳ Processing...")
            
            # Prepare A2A message
            send_message_payload = {
                'message': {
                    'role': 'user',
                    'parts': [{'type': 'text', 'text': message}],
                    'messageId': uuid4().hex,
                },
                'sessionId': self.session_id
            }
            
            request = SendMessageRequest(id=str(uuid.uuid4()),params=MessageSendParams(**send_message_payload))
            response = await self.client.send_message(request)
            
            response_data = response.model_dump(mode='json', exclude_none=True)
            response_text = self._extract_response_text(response_data)
            
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'user_message': message,
                'orchestrator_response': response_text,
                'raw_response': response_data
            })
            
            return response_text
            
        except Exception as e:
            error_msg = f"Error sending message: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
    
    def _extract_response_text(self, response_data) -> str:
        """Extract text from A2A response"""
        try:

            if 'result' in response_data and isinstance(response_data['result'], dict):
                result = response_data['result']

                if 'parts' in result and isinstance(result['parts'], list) and len(result['parts']) > 0:
 
                    first_part = result['parts'][0]

                    if 'text' in first_part:
                        return first_part['text']
                    
            if isinstance(response_data, dict):
                if 'message' in response_data and 'parts' in response_data['message']:
                    parts = response_data['message']['parts']
                    if parts and len(parts) > 0 and 'text' in parts[0]:
                        return parts[0]['text']

                if 'response' in response_data:
                    return str(response_data['response'])

                if 'content' in response_data:
                    return str(response_data['content'])

            return str(response_data)

        except (KeyError, IndexError) as e:
            return f"Error parsing response structure: {str(e)}"
        except Exception as e:
            return f"Unexpected error while parsing response: {str(e)}"
    
    def print_conversation_history(self):
        """Print the conversation history"""
        print("\n" + "="*60)
        print("CONVERSATION HISTORY")
        print("="*60)
        
        for i, entry in enumerate(self.conversation_history, 1):
            print(f"\n[{i}] {entry['timestamp']}")
            print(f"👤 User: {entry['user_message']}")
            print(f"🤖 Orchestrator: {entry['orchestrator_response']}")
        
        print("="*60)
    
    def save_conversation(self, filename: Optional[str] = None):
        """Save conversation to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump({
                    'session_id': self.session_id,
                    'orchestrator_url': self.orchestrator_url,
                    'conversation_history': self.conversation_history
                }, f, indent=2)
            
            print(f"💾 Conversation saved to {filename}")
            
        except Exception as e:
            print(f"❌ Error saving conversation: {e}")

async def chat_loop(client):
    """Main chat loop"""
    print("\n🎯 Connected! You can now chat with the orchestrator.")
    print("Commands:")
    print("  - Type 'quit' or 'exit' to end")
    print("  - Type 'history' to see conversation history")
    print("  - Type 'save' to save conversation")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit']:
                print("👋 Goodbye!")
                break
            
            elif user_input.lower() == 'history':
                if hasattr(client, 'print_conversation_history'):
                    client.print_conversation_history()
                else:
                    print("History not available for this client type")
                continue
            
            elif user_input.lower() == 'save':
                if hasattr(client, 'save_conversation'):
                    client.save_conversation()
                else:
                    print("Save not available for this client type")
                continue

            response = await client.send_message(user_input)
            print(f"\n🤖 Orchestrator: {response}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")



async def main():
    try:
        async with InteractiveA2ATestClient() as client:
            await chat_loop(client)
    except Exception as e:
        print(f"❌ A2A connection failed: {e}")
        print("Falling back to Direct HTTP...")


if __name__=="__main__":
    asyncio.run(main())
    