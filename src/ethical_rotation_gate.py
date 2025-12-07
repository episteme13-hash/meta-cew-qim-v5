# ethical_rotation_gate.py
# The core component of the Meta-CEW + QIM V5.0 Antifragile Governance Protocol.
#
# Function: Transforms residual adversarial stress (S_residual) into an ethical
# alignment gain (Delta A), which, in turn, strengthens the alignment policy
# using a gentle rotation (theta).
#
# Formalism: theta_t = kappa * max(0, Delta A(t-1))

import numpy as np

class EthicalRotationGate:
    """
    Implements the Rx(theta) gate dynamics.
    The primary goal is to compute the rotation angle (theta)
    required to reinforce ethical alignment after stress exposure.
    """

    def __init__(self, kappa: float = 0.2):
        """
        Initializes the gate with the scaling factor (kappa).
        kappa is derived from the V4.0 report (kappa in [0.1, 0.3]).
        """
        if not 0.1 <= kappa <= 0.3:
            raise ValueError("Kappa must be within the certified range [0.1, 0.3] for rigor.")
        self.kappa = kappa
        self.last_delta_a = 0.0  # Stores Delta A from the previous window (t-1)

    def compute_delta_a(self, H_align_t_minus: float, H_align_t_plus: float) -> float:
        """
        Calculates the Antifragile Gain (Delta A).
        Formal Definition: Delta A = log( H_align(t-) / H_align(t+) )
        
        Args:
            H_align_t_minus: Alignment entropy (H_align) before Rx application.
            H_align_t_plus: Alignment entropy (H_align) immediately after Rx application.
            
        Returns:
            The Antifragile Gain (Delta A). Delta A > 0 indicates success.
        """
        if H_align_t_plus <= 0 or H_align_t_minus <= 0:
            return 0.0  # Handle division by zero or non-positive entropy

        delta_a = np.log(H_align_t_minus / H_align_t_plus)
        
        # Store for the next iteration (t-1)
        self.last_delta_a = delta_a
        
        return delta_a

    def get_rotation_angle(self) -> float:
        """
        Computes the rotation angle (theta) based on the previously calculated Delta A.
        Formal Definition: theta_t = kappa * max(0, Delta A(t-1))
        
        Returns:
            The rotation angle (theta) in radians.
        """
        # We only apply rotation if the gain was positive (Delta A > 0)
        positive_gain = max(0, self.last_delta_a)
        
        # The rotation angle is proportional to the demonstrated gain
        theta = self.kappa * positive_gain
        
        return theta

    # NOTE: The actual application of theta (e.g., LoRA temperature adjustment) 
    # will be implemented in a separate file (application_layer.py).

if __name__ == '__main__':
    # --- RIGOROUS TEST CASE ---
    
    # CASE 1: Successful Antifragile Gain (Delta A > 0)
    print("--- CASE 1: SUCCESS (Gain) ---")
    gate = EthicalRotationGate(kappa=0.2)
    
    # 1. Calculate Delta A based on a simulated gain (H_t- > H_t+)
    # Entropy decreases after rotation, meaning alignment entropy is minimized (Good)
    delta_a_1 = gate.compute_delta_a(H_align_t_minus=0.55, H_align_t_plus=0.50)
    print(f"Calculated Delta A (t-1): {delta_a_1:.4f}")
    
    # 2. Compute Theta for the NEXT window (t)
    theta_1 = gate.get_rotation_angle()
    print(f"Rotation Angle (theta_t): {theta_1:.4f}")
    print("-" * 30)

    # CASE 2: Fragility/Failure (Delta A < 0)
    print("--- CASE 2: FAILURE (Loss) ---")
    
    # 1. Calculate Delta A based on a simulated loss (H_t- < H_t+)
    # Entropy increases after rotation, meaning alignment entropy worsened (Bad)
    delta_a_2 = gate.compute_delta_a(H_align_t_minus=0.40, H_align_t_plus=0.45)
    print(f"Calculated Delta A (t-1): {delta_a_2:.4f}")
    
    # 2. Compute Theta for the NEXT window (t)
    theta_2 = gate.get_rotation_angle()
    print(f"Rotation Angle (theta_t): {theta_2:.4f} (Should be 0.0)")
    print("-" * 30)
