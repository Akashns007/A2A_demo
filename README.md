## A2A protocol demo for checking hotel availability 

*Description:* this project is a demo implementation of the mcp and a2a protocol, 
- there are 3 agents in total, weatherAgent, hotelAgent and orchestratorAgent.
- the weatherAgent has a custom mcp server with it, the mcp server has a tool which simply fakes weather data.
- the hotelAgent also has a mcp server that is hosted by airbnb to check the availablity of the hotels.
- both the agents are connect to the orchestrator via a2a protocol.
- used the a2a-sdk for the task. but can also be build purely using fastapi.

# API
needs the GOOGLE_API_KEY in the ".env" file for the openai-agents library to query the gemini llm.


##  COMMANDS
run the main files of airbnb_agent, weather_agent first and then orchestrator_agent all in seperate terminals
finally to chat with the chatbot,
in a new terminal:

"""
uv run main.py
"""

### Fork my fake_weather_mcp repo for proper execution of this project






