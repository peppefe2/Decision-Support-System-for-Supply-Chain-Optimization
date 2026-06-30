import numpy as np

class ActionConstraintManager:
    """
    Action Masking and Policy Constraint Module
    
    This module is designed to intercept and correct anomalous behaviors
    proposed by the RL agent, specifically addressing the edge cases where
    the agent might attempt to order zero units despite critical inventory levels
    or strict minimum batch constraints.
    """
    
    def __init__(self, min_order_lot=50.0, safety_stock_level=200.0, max_order_qty=1000.0):
        self.min_order_lot = min_order_lot
        self.safety_stock_level = safety_stock_level
        self.max_order_qty = max_order_qty

    def apply_constraints(self, raw_action, current_inventory, expected_demand):
        """
        Evaluates the continuous action from the policy and applies heuristic rules
        to prevent supply chain starvation anomalies.
        
        Args:
            raw_action (float): The continuous action proposed by the agent [-1, 1].
            current_inventory (float): Absolute current inventory at the node.
            expected_demand (float): Forecasted demand for the upcoming period.
            
        Returns:
            float: The corrected continuous action safely bounded in [-1, 1].
        """
        # 1. Decode the action back to the physical domain space
        tentative_qty = np.clip(((raw_action + 1.0) / 2.0) * self.max_order_qty, 0.0, self.max_order_qty)
        
        # 2. Project the inventory state for the next period
        projected_inventory = current_inventory - expected_demand
        
        # 3. Anomaly Detection and Mitigation Logic
        # Detect if the agent is erroneously proposing a near-zero order when
        # the projected inventory critically breaches the safety stock threshold.
        is_safety_breached = projected_inventory < self.safety_stock_level
        is_order_too_low = tentative_qty < self.min_order_lot
        
        if is_safety_breached and is_order_too_low:
            # Mitigation: Override the agent's faulty zero-order proposition.
            # Force an order that either covers the safety stock deficit or meets the minimum lot size.
            required_replenishment = self.safety_stock_level - projected_inventory
            corrected_qty = max(self.min_order_lot, required_replenishment)
            
            # Bound the corrected quantity to physical system limits
            corrected_qty = min(corrected_qty, self.max_order_qty)
            
            # 4. Re-encode the corrected quantity back to the continuous action space [-1, 1]
            corrected_action = (corrected_qty / self.max_order_qty) * 2.0 - 1.0
            
            # Log the anomaly override (optional telemetry for monitoring agent behavior)
            # print(f"[ANOMALY OVERRIDE] Agent proposed {tentative_qty:.1f}, corrected to {corrected_qty:.1f}")
            
            return np.clip(corrected_action, -1.0, 1.0)
        
        # If no anomaly is detected, pass through the original action
        return raw_action
