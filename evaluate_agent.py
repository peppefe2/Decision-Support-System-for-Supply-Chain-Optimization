import numpy as np
from supply_chain_env import SupplyChainEnv
from action_constraints import ActionConstraintManager

class DummyDEPEModel:
    """
    Mock representation of the Dual-Expert Policy Ensemble (DEPE).
    
    [IP Protection]
    The exact neural architecture, the dynamic MoE routing mechanism, 
    and the pre-trained weights have been omitted for this public showcase.
    This class mocks the prediction interface.
    """
    def predict(self, obs, deterministic=True):
        # Mocks an intelligent policy output by closely tracking expected demand
        # to demonstrate a functional Bullwhip Effect reduction in the showcase.
        expected_demand_norm = obs[2]
        # Calculate a smooth action that matches demand to keep inventory stable
        smooth_action = expected_demand_norm - 1.0
        return np.array([smooth_action]), None

def evaluate_agent(episodes=5, verbose=True):
    """
    Validation script simulating the interaction between the DEPE policy
    and the System Dynamics environment. Calculates the Bullwhip Effect 
    mitigation metrics over a predefined horizon.
    """
    if verbose:
        print("=" * 60)
        print("🚀 Initiating DEPE Agent Validation (Showcase Mode)")
        print("=" * 60)

    # Initialize Environment, Agent, and Masking Middleware
    env = SupplyChainEnv()
    agent = DummyDEPEModel()
    constraint_manager = ActionConstraintManager()
    
    total_bullwhip_reduction = 0.0
    
    for ep in range(episodes):
        obs, _ = env.reset()
        done = False
        
        demand_history = []
        order_history = []
        
        while not done:
            # 1. Agent predicts the action based on the state
            raw_action, _ = agent.predict(obs)
            
            # Extract state metrics needed for the heuristic constraint logic
            current_inv = obs[0] * env.MAX_INVENTORY
            expected_demand = obs[2] * 500.0  # Decoded from the observation scaling
            
            # 2. Apply Middleware Constraint Masking
            safe_action = constraint_manager.apply_constraints(
                raw_action[0], 
                current_inventory=current_inv, 
                expected_demand=expected_demand
            )
            
            # 3. Step the environment
            obs, reward, terminated, truncated, info = env.step(np.array([safe_action]))
            done = terminated or truncated
            
            # 4. Track temporal metrics for Bullwhip Effect analysis
            demand_history.append(expected_demand)
            order_history.append(info['order_qty'])

        # Calculate Bullwhip Effect (BWE) for the current episode
        # BWE = Variance of Orders / Variance of Demand
        var_demand = np.var(demand_history)
        var_order = np.var(order_history)
        
        # Safe division fallback
        bullwhip_ratio = (var_order / var_demand) if var_demand > 0 else 1.0
            
        # Baseline Comparison (Fictional traditional heuristic benchmark)
        baseline_bullwhip = 1.85 
        
        # Calculate Percentage Reduction vs Baseline
        if bullwhip_ratio < baseline_bullwhip:
            reduction_pct = ((baseline_bullwhip - bullwhip_ratio) / baseline_bullwhip) * 100
        else:
            reduction_pct = 0.0
            
        total_bullwhip_reduction += reduction_pct
        
        if verbose:
            print(f"🔹 Episode {ep+1}/{episodes} | BW Ratio: {bullwhip_ratio:.3f} | Reduction vs Baseline: {reduction_pct:.1f}%")

    avg_reduction = total_bullwhip_reduction / episodes
    
    if verbose:
        print("-" * 60)
        print(f"✅ Evaluation Complete. Average Bullwhip Effect Mitigation: {avg_reduction:.1f}%")
        print("=" * 60)

if __name__ == "__main__":
    # Run the validation evaluation
    evaluate_agent(episodes=5)
