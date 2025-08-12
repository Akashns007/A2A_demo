import httpx
import asyncio
from typing import Dict, List, Optional
from a2a.client import A2AClient
from a2a.types import AgentCard
import json
import pickle


class AgentDiscoveryService:
    """Service for discovering and managing A2A agents"""
    
    def __init__(self):
        self.known_agent_urls = [
            "http://localhost:7001",  # Weather Agent
            "http://localhost:7002",  # Airbnb Agent
        ]
        self.discovered_agents: Dict[str, AgentCard] = {}
        self.domain_name = "http://localhost:"
        self.host = "localhost"
        self.START_PORT = 7000
        self.END_PORT = 8000
        self.CAHCE_FILE = "agents.pkl"
    
    async def discover_agents(self) -> Dict[str, AgentCard]:
        """Discover all available A2A agents"""
        print("Discovering available agents...")
        
        discovered = {}
        
        async with httpx.AsyncClient(timeout=10.0) as httpx_client:
            for agent_url in self.known_agent_urls:
                try:
                    agent_card = await self._get_agent_card(httpx_client, agent_url)
                    if agent_card:
                        discovered[agent_card.name] = agent_card
                        print(f"✓ Discovered: {agent_card.name} at {agent_url}")
                    else:
                        print(f"✗ Failed to get agent card from {agent_url}")
                        
                except Exception as e:
                    print(f"✗ Error discovering agent at {agent_url}: {e}")
        
        self.discovered_agents = discovered
        return discovered
    
    async def _get_agent_card(self, httpx_client: httpx.AsyncClient, agent_url: str) -> Optional[AgentCard]:
        """Get agent card from a specific URL"""
        try:
            client = A2AClient(httpx_client =httpx_client, url = agent_url)
            if client and hasattr(client, '/.well-known/agent_card.json'):
                return client.agent_card
            
            # Fallback: try direct HTTP request to agent card endpoint
            response = await httpx_client.get(f"{agent_url}/.well-known/agent-card.json")
            if response.status_code == 200:
                card_data = response.json()
                return AgentCard(**card_data)
            
            else:
                return 
            
        except Exception as e:
            print(f"Error getting agent card from {agent_url}: {e}")
        
        return None
    
    def format_agent_cards_for_prompt(self) -> str:
        """Format discovered agent cards for use in agent instructions"""
        if not self.discovered_agents:
            return "No agents currently available."
        
        formatted_cards = []
        for name, card in self.discovered_agents.items():
            skills_desc = "\n".join([f"    - {skill.name}: {skill.description}" for skill in card.skills])
            
            agent_info = {
                            "Agent": {name},
                            "URL": {card.url},
                            "Description": {card.description},
                            "Skills":{skills_desc},
                            "Examples": {', '.join(card.skills[0].examples[:3]) if card.skills else 'None'}
            }
            formatted_cards.append(agent_info)
        
        return formatted_cards
    


    async def _check_port_open(self, port: int) -> bool:
        try:
            reader, writer = await asyncio.open_connection(self.host, port)
            writer.close()
            await writer.wait_closed()
            return True
        except:
            return False

    async def _find_open_ports(self) -> list[int]:
        tasks = [self._check_port_open(port) for port in range(self.START_PORT, self.END_PORT)]
        results = await asyncio.gather(*tasks)
        return [port for port, is_open in zip(range(self.START_PORT, self.END_PORT), results) if is_open]


    async def discover_agents_port_scanner(self):
        discovered = {}
        open_ports = await self._find_open_ports()

        async with httpx.AsyncClient(timeout=10.0) as httpx_client:
            for port in open_ports:
                try:
                    agent_url = self.domain_name + str(port)
                    agent_card = await self._get_agent_card(httpx_client, agent_url)
                    if agent_card:
                        discovered[agent_card.name] = agent_card
                        print(f"✓ Discovered: {agent_card.name} at {agent_url}")
                        
                except Exception as e:
                    print(f"✗ Error discovering agent at {agent_url}: {e}")

            with open(self.CAHCE_FILE, 'wb') as f:
                pickle.dump(discovered, f)

        self.discovered_agents = discovered
        return discovered


    def cached_agents(self):
        with open(self.CAHCE_FILE, 'rb') as f:
            agent_cards = pickle.load(f)

        return agent_cards 
        

if __name__ == "__main__":
    service = AgentDiscoveryService()

    asyncio.run(service.discover_agents_port_scanner())

    print("\n--- Cached agents from file ---")
    cached = service.cached_agents()
    for name, card in cached.items():
        print(f"{name} → {card.url}")



        



    

