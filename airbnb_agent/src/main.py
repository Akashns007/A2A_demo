import asyncio
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill 
from services.agent_executer import AirbnbAgentExecutor


def create_airbnb_agent_card():
    """Create the agent card defining the Airbnb agent's capabilities"""
    
    accommodation_search_skill = AgentSkill(
        id="search_airbnb_accommodations",
        name="SearchAirbnbAccommodations",
        description="""A skill to search for accommodations on Airbnb including hotels, rooms, and vacation rentals.
        Can handle date ranges, location specifications, guest counts (adults and children), pet requirements,
        and provides detailed property information including pricing, amenities, and host details.""",
        tags=["airbnb", "accommodation", "hotels", "travel", "booking", "vacation-rentals"],
        examples=[
            "Find me a hotel in London for August 10-14, 2025 for 3 adults and 2 kids",
            "Search for Airbnb properties in Paris for 2 people from Dec 1-5",
            "Get accommodation options in Tokyo for a family of 4 with pets",
            "Show me vacation rentals in New York with 2 bedrooms for next weekend",
            "Find budget-friendly rooms in Barcelona for solo travel",
            "Search for luxury accommodations in Dubai for 6 guests"
        ],
    )
    
    agent_card = AgentCard(
        name="AirbnbAgent",
        description="""An Airbnb assistant agent that helps users find and compare accommodations.
        Specializes in searching Airbnb for hotels, rooms, and vacation rentals worldwide.
        Provides detailed property information including pricing, amenities, location details, and host information.
        Can handle complex queries with specific dates, guest counts, and requirements.""",
        url="http://localhost:7002/",  
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        skills=[accommodation_search_skill],
        capabilities=AgentCapabilities(),
        version="1.0.0"
    )
    
    return agent_card


def main():
    """Main function to start the A2A Airbnb agent server"""
    
    airbnb_agent_executor = AirbnbAgentExecutor()  
    agent_card = create_airbnb_agent_card()

    request_handler = DefaultRequestHandler(
        agent_executor = airbnb_agent_executor,
        task_store=InMemoryTaskStore(),
    )
    
    app = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    print("Starting Airbnb Agent A2A Server...")
    print(f"Agent Card: {agent_card.name}")
    print(f"Server URL: {agent_card.url}")
    print("Available skills:")
    for skill in agent_card.skills:
        print(f"  - {skill.name}: {skill.description}")
    
    # Start the server
    uvicorn.run(
        app.build(),
        host="0.0.0.0",
        port=7002,
        log_level="info"
    )


if __name__ == "__main__":
    main()
