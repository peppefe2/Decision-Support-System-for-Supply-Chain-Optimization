## Project Overview
This repository presents a showcase of a Cognitive Decision Support System designed to optimize multi-echelon supply chains. By integrating Reinforcement Learning (RL) with System Dynamics, the architecture dynamically addresses complex operational bottlenecks, specifically targeting the mitigation of the Bullwhip Effect and enhancing overall supply chain resilience.

**Note on Intellectual Property & Data Privacy:**
This project is part of ongoing academic research and involves proprietary architectural logic (such as the Dual-Expert Policy Ensemble - DEPE). To protect intellectual property and unpublished research components, the exact neural architectures, pretrained model weights, and proprietary System Dynamics equations have been redacted. The codebase provided here serves as a structural demonstration of the environment mechanics, the action constraint logic, and the validation pipeline.

## Architecture & Core Mechanics
The system operates at the intersection of continuous simulation and intelligent control. The codebase demonstrates three critical components of the pipeline:

### 1. The Simulation Environment
The RL agent interacts with a custom Gymnasium environment that acts as a simplified Digital Twin of the supply chain.
* **Observation Space:** The agent monitors the normalized inventory levels, work-in-progress (WIP) orders in transit, and simulated stochastic expected demand.
* **Action Space:** The agent outputs a continuous action regulating the order replenishment quantity.
* **System Dynamics Integration:** The environment state transitions are governed by a dynamic engine that simulates stochastic demand, lead times, and associated holding/backorder costs.

### 2. Action Constraint Middleware
A crucial engineering challenge in applying RL to physical environments is ensuring operational safety. This repository features an ActionConstraintManager module designed to intercept and override anomalous agent behaviors.
* **Anomaly Mitigation:** Specifically, the middleware detects edge cases where the RL agent might erroneously propose a near-zero order despite critically low projected inventory (breaching safety stock).
* **Heuristic Override:** When an anomaly is detected, the manager dynamically corrects the continuous action to ensure compliance with strict minimum batch constraints and safety stock thresholds before the order is executed in the environment.

### 3. Validation Pipeline & Bullwhip Effect Analysis
The evaluation script orchestrates the interaction between the policy ensemble and the constraint-bounded environment to calculate operational metrics.
* **Performance Metric:** The primary metric evaluated is the Bullwhip Effect, calculated as the variance of orders relative to the variance of demand.
* **Benchmarking:** The evaluation compares the agent's performance against a baseline traditional heuristic, tracking the percentage reduction of the Bullwhip Effect over a simulated temporal horizon.

## Repository Structure
* `supply_chain_env.py`: The custom Gymnasium environment defining the supply chain state space, continuous action space, and simplified System Dynamics logic.
* `action_constraints.py`: The middleware logic that applies heuristic safety bounds to the agent's raw continuous actions to prevent supply chain starvation.
* `evaluate_agent.py`: The execution script that runs the interaction loop, applies the constraint masking, and calculates the resulting mitigation of the Bullwhip Effect.

## Execution & Testing
To run the validation demonstration:
1. Ensure the required dependencies are installed (e.g., numpy, gymnasium).
2. Execute the validation script:
   ```bash
   python evaluate_agent.py

## Project Collaborators
This research and architecture development was conducted in collaboration with:

* **Giuseppe Emanuele Ferro**
  [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/giuseppe-emanuele-ferro/?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BD4cRCj6PRAKmGqCoTYommQ%3D%3D)
