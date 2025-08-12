import asyncio
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill 
from services.agent_executor import WeatherAgentExecutor


def create_weather_agent_card():
    """Create the agent card defining the weather agent's capabilities"""
    weather_skill = AgentSkill(
        id="get_weather_sept_2025",
        name="GetWeatherSeptember2025",
        description="""A skill to fetch weather information for a specified date range
        within the month of September 2025. It requires 'start_day' and 'end_day'
        in 'DD' format to be used as parameters.""",
        tags=["weather", "september", "2025", "forecast"],
        examples=[
            "What is the weather like on September 15?",
            "Give me the forecast for September 10th to the 15th.",
            "Weather for Sep 01 to Sep 05",
            "How's the weather from September 5th to 10th?",
            "Tell me about the weather on Sep 20"
        ],
    )
    
    agent_card = AgentCard(
        name="WeatherAgent",
        description="""A weather agent that provides weather information for the month of September 2025.
        It uses a specific skill to fetch data from an MCP server and is limited to weather-related queries only.
        Can handle date ranges and single date queries within September 2025.""",
        url="http://localhost:7001/",  
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        skills=[weather_skill],
        capabilities=AgentCapabilities(),
        version="1.0.0"
    )
    
    return agent_card


def main():
    """Main function to start the A2A weather agent server"""
    
    weather_agent_executor = WeatherAgentExecutor()
    # Create the agent card
    agent_card = create_weather_agent_card()
    
    # Create the request handler with the weather agent executor
    request_handler = DefaultRequestHandler(
        agent_executor = weather_agent_executor,
        task_store=InMemoryTaskStore(),
    )
    
    # Create the A2A application
    app = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )
    
    # Configure and start the server
    print("Starting Weather Agent A2A Server...")
    print(f"Agent Card: {agent_card.name}")
    print(f"Server URL: {agent_card.url}")
    print("Available skills:")
    for skill in agent_card.skills:
        print(f"  - {skill.name}: {skill.description}")
    
    # Start the server
    uvicorn.run(
        app.build(),  # The Starlette app instance
        host="0.0.0.0",
        port=7001,
        log_level="info"
    )


if __name__ == "__main__":
    main()


# requirements.txt (add these dependencies)
"""
fastapi
uvicorn
starlette
pydantic
python-dotenv
asyncio
# Add your existing dependencies here as well
"""

# Optional: config.py for configuration management

# Alternative main.py with FastAPI (if you prefer FastAPI over Starlette)
"""
from fastapi import FastAPI
from a2a.server.adapters.fastapi import FastAPIAdapter

def main_fastapi():
    agent_card = create_weather_agent_card()
    
    request_handler = DefaultRequestHandler(
        agent_executor_factory=lambda: WeatherAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )
    
    # Create FastAPI app
    app = FastAPI(title="Weather Agent A2A Server")
    
    # Add A2A adapter
    adapter = FastAPIAdapter(
        agent_card=agent_card,
        request_handler=request_handler
    )
    
    adapter.mount(app)
    
    uvicorn.run(app, host="0.0.0.0", port=7001)
"""
