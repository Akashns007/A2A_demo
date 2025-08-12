import asyncio
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill 
from services.agent_executor import AdvancedOrchestratorAgentExecutor


def create_advanced_orchestrator_agent_card():
    """Create the agent card defining the advanced orchestrator agent's capabilities"""
    
    intelligent_routing_skill = AgentSkill(
        id="intelligent_agent_routing",
        name="IntelligentAgentRouting",
        description="""Advanced agent routing that discovers available A2A agents dynamically and routes 
        queries intelligently. Uses agent discovery to find weather and accommodation agents, then 
        orchestrates multi-step workflows for comprehensive travel planning.""",
        tags=["orchestration", "routing", "agent-discovery", "travel-planning", "workflow"],
        examples=[
            "Plan a trip from Bangalore to Chennai from Sep 15-20, 2025",
            "I need weather info and accommodation for my Tokyo vacation",
            "Help me plan a complete trip including weather check and hotel booking",
            "Coordinate weather forecast and room availability for my travel dates"
        ],
    )
    
    dynamic_agent_discovery_skill = AgentSkill(
        id="dynamic_agent_discovery",
        name="DynamicAgentDiscovery", 
        description="""Automatically discovers and manages connections to available A2A agents in the network. 
        Can dynamically adapt to agent availability and route requests accordingly.""",
        tags=["discovery", "dynamic", "agent-management", "a2a-protocol"],
        examples=[
            "Discover what agents are available for travel planning",
            "Find specialized agents for weather and accommodation services",
            "Adapt to agent availability in real-time"
        ],
    )
    
    workflow_coordination_skill = AgentSkill(
        id="multi_step_workflow_coordination",
        name="MultiStepWorkflowCoordination",
        description="""Coordinates complex multi-step workflows across multiple agents. Can execute 
        sequential and parallel agent calls based on business logic and user needs.""",
        tags=["workflow", "coordination", "multi-step", "business-logic"],
        examples=[
            "Execute weather check before accommodation search workflow",
            "Coordinate parallel queries to multiple specialized agents",
            "Implement conditional logic based on agent responses"
        ],
    )
    
    agent_card = AgentCard(
        name="AdvancedOrchestratorAgent",
        description="""An advanced travel planning orchestrator with dynamic agent discovery and intelligent routing capabilities. 
        Automatically discovers available A2A agents, creates sophisticated multi-step workflows, and provides comprehensive 
        travel planning services by coordinating specialized weather and accommodation agents. Features intelligent conditional 
        logic and adaptive routing based on agent responses.""",
        url="http://localhost:7000/",  
        skills=[intelligent_routing_skill, dynamic_agent_discovery_skill, workflow_coordination_skill],
        capabilities=AgentCapabilities(),
        version="2.0.0",
        defaultInputModes=["text", "json"],
        defaultOutputModes=["text", "json"]

    )
    
    return agent_card


def main():
    """Main function to start the advanced A2A orchestrator agent server"""


    agent_card = create_advanced_orchestrator_agent_card()


    
    request_handler = DefaultRequestHandler(
        agent_executor=AdvancedOrchestratorAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )
    
    app = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )
    
    # Configure and start the server
    print("Starting Advanced Orchestrator Agent A2A Server...")
    print(f"Agent Card: {agent_card.name}")
    print(f"Server URL: {agent_card.url}")
    print("\nFeatures:")

    
    print(f"\nWill discover agents at:")
    print("  - WeatherAgent: http://localhost:7001")
    print("  - AirbnbAgent: http://localhost:7002")
    
    print("\nAvailable skills:")
    for skill in agent_card.skills:
        print(f"  - {skill.name}")
    
    print("\n" + "="*70)
    print("ORCHESTRATOR READY - Send travel planning queries!")
    print("="*70)
    
    # Start the server
    uvicorn.run(
        app.build(), 
        host="0.0.0.0",
        port=7000,  
        log_level="info",
    )


if __name__ == "__main__":
    main()

