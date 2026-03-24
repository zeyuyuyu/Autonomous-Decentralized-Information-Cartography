import os
import sys
import time
import random
from collections import deque
from typing import List, Dict, Tuple

from src.agent import Agent
from src.environment import Environment
from src.governance import GovernanceProtocol
from src.visualization import Visualizer

def main():
    """
    Main entry point for the Autonomous Decentralized Information Cartography (ADIC) project.
    """
    # Initialize the environment
    env = Environment()

    # Initialize the governance protocol
    governance = GovernanceProtocol()

    # Spawn the initial swarm of agents
    agents: List[Agent] = [Agent(env, governance) for _ in range(100)]

    # Run the main loop
    while True:
        # Agents explore the environment and gather information
        for agent in agents:
            agent.explore()

        # Agents share information and collaborate to build the knowledge map
        for agent in agents:
            agent.share_information()
            agent.update_map()

        # Visualize the current state of the knowledge map
        Visualizer.render(env.knowledge_map)

        # Apply governance rules and protocols
        governance.maintain_system(env, agents)

        # Wait for the next iteration
        time.sleep(1)

if __name__ == "__main__":
    main()