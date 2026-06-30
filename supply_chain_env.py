import numpy as np
import gymnasium as gym
from gymnasium import spaces

class SupplyChainEnv(gym.Env):
    """
    Cognitive Decision Support System - Supply Chain Environment
    
    A custom Gymnasium Environment for Reinforcement Learning.
    This environment simulates a multi-echelon supply chain focusing on
    inventory management, anomaly mitigation, and the Bullwhip Effect.
    
    Note: Proprietary System Dynamics equations and precise cost parameters 
    have been obfuscated for this public showcase.
    """
    
    def __init__(self):
        super().__init__()
        
        # Obfuscated generic constants (Original values removed to protect IP)
        self.COST_HOLDING_DUMMY = 1.0
        self.COST_BACKORDER_DUMMY = 5.0
        self.MAX_INVENTORY = 5000.0
        self.MAX_ORDER_QTY = 1000.0
        
        # Observation Space Setup
        # [0]: Normalized Inventory level at current node
        # [1]: Normalized In-transit orders (WIP)
        # [2]: Normalized expected demand
        self.observation_space = spaces.Box(
            low=0.0, 
            high=np.inf, 
            shape=(3,), 
            dtype=np.float32
        )
        
        # Action Space Setup
        # Continuous action controlling the order quantity (normalized between -1 and 1)
        self.action_space = spaces.Box(
            low=-1.0, 
            high=1.0, 
            shape=(1,), 
            dtype=np.float32
        )
        
        # Environment State
        self.current_inventory = 0.0
        self.wip_orders = 0.0
        self.current_step = 0
        self.max_steps = 100

    def reset(self, seed=None, options=None):
        """
        Resets the environment to an initial steady state.
        """
        super().reset(seed=seed)
        self.current_step = 0
        self.current_inventory = 1000.0  # Steady state initial inventory
        self.wip_orders = 200.0          # Initial in-transit baseline
        
        obs = self._get_obs()
        info = {}
        return obs, info

    def _get_obs(self):
        """
        Constructs the observation vector for the RL agent.
        """
        # Exogenous stochastic demand simulation
        simulated_demand = np.random.normal(100, 10)
        
        return np.array([
            self.current_inventory / self.MAX_INVENTORY,
            self.wip_orders / self.MAX_ORDER_QTY,
            simulated_demand / 500.0
        ], dtype=np.float32)

    def _simulate_system_dynamics(self, order_qty):
        """
        Executes a discrete step of the System Dynamics engine.
        
        [IP Protection] 
        The actual proprietary differential equations mapping lead times, 
        disruptions, and non-linear backlogs have been replaced with a 
        simplified linear dynamic update for demonstration purposes.
        """
        # Simplified stochastic demand
        demand = np.random.normal(100, 10)
        
        # State transition
        self.current_inventory += self.wip_orders - demand
        self.wip_orders = order_qty  # Simplified lead time of 1 step
        
        # Objective Function Cost Calculation
        holding_cost = max(0, self.current_inventory) * self.COST_HOLDING_DUMMY
        backorder_cost = max(0, -self.current_inventory) * self.COST_BACKORDER_DUMMY
        total_cost = holding_cost + backorder_cost
        
        return total_cost

    def step(self, action):
        """
        Environment transition step responding to the agent's action.
        """
        self.current_step += 1
        
        # Decode policy output to physical order quantity
        order_qty = np.clip(((action[0] + 1.0) / 2.0) * self.MAX_ORDER_QTY, 0.0, self.MAX_ORDER_QTY)
        
        # Transition the System Dynamics state
        cost = self._simulate_system_dynamics(order_qty)
        
        # Reward Engineering: Minimize total operational cost
        reward = -cost
        
        terminated = self.current_step >= self.max_steps
        truncated = False
        
        obs = self._get_obs()
        info = {"order_qty": order_qty, "cost": cost}
        
        return obs, reward, terminated, truncated, info
