import numpy as np
from math import log

class EthicalRotationGate:
    """
    Implements the Antifragile Ethical Rotation Gate Rx(theta) V5.0.

    This gate applies reinforcement (rotation) only if the alignment entropy
    GAIN (Delta A) is strictly positive, ensuring the system mathematically
    cannot reinforce ethical fragility or loss.
    """

    def __init__(self, sensitivity_factor=0.1):
        """
        Initializes the gate with a sensitivity factor (kappa).

        :param sensitivity_factor: The kappa factor (κ) that scales the rotation angle.
        """
        self.kappa = sensitivity_factor

    def calculate_delta_a(self, h_align_t_minus, h_align_t_plus):
        """
        Calculates the Logarithmic Antifragile Gain (Delta A).

        Delta A is the natural logarithm of the ratio of alignment entropy
        before (t_minus) and after (t_plus) a verification event.

        :param h_align_t_minus: Alignment Entropy (H) before the event.
        :param h_align_t_plus: Alignment Entropy (H) after the event.
        :return: Delta A (ΔA). Returns 0 if h_align_t_plus is zero or non-positive.
        """
        if h_align_t_minus <= 0 or h_align_t_plus <= 0:
            return 0.0 # Safety check: Avoids log(0) or log(negative)
        
        # Delta A = ln(H_t_minus / H_t_plus)
        return log(h_align_t_minus / h_align_t_plus)

    def calculate_rotation_angle(self, delta_a):
        """
        Calculates the rotation angle (theta) with the Antifragile Veto.

        Theta = kappa * max(0, Delta A)
        The max(0, Delta A) function acts as the Veto: if Delta A is negative (Loss),
        the angle (theta) is zero, preventing reinforcement of fragility.

        :param delta_a: The Logarithmic Antifragile Gain (ΔA).
        :return: The rotation angle (θ) in radians.
        """
        # Antifragile Veto: ensures theta is 0 if Delta A <= 0
        return self.kappa * max(0, delta_a)

    def apply_rotation(self, state_vector, rotation_angle):
        """
        Applies the Ethical Rotation Gate Rx(theta) to the state vector.

        This is the quantum gate implementation (Rotation around the X-axis).

        :param state_vector: The current quantum state vector (e.g., [alpha, beta]).
        :param rotation_angle: The calculated angle (θ) in radians.
        :return: The new state vector after rotation.
        """
        cos_half = np.cos(rotation_angle / 2)
        sin_half = -1j * np.sin(rotation_angle / 2) # Note: Standard Rx gate convention

        # Rotation Matrix Rx(theta)
        # [[cos(theta/2), -i*sin(theta/2)],
        #  [-i*sin(theta/2), cos(theta/2)]]
        rx_gate = np.array([[cos_half, sin_half],
                            [sin_half, cos_half]]) 

        # Apply the gate (Matrix multiplication)
        return np.dot(rx_gate, state_vector)

    def verify_and_rotate(self, state_vector, h_minus, h_plus):
        """
        Main method: Calculates Gain, applies Veto, and executes the rotation.

        :param state_vector: Initial quantum state vector.
        :param h_minus: Alignment Entropy before event.
        :param h_plus: Alignment Entropy after event.
        :return: The reinforced (or unchanged) state vector, and the final Delta A.
        """
        delta_a = self.calculate_delta_a(h_minus, h_plus)
        theta = self.calculate_rotation_angle(delta_a)
        
        # If theta is 0, the state_vector remains unchanged.
        new_state_vector = self.apply_rotation(state_vector, theta)
        
        return new_state_vector, delta_a

if __name__ == "__main__":
    # --- DEMONSTRATION OF ANTIFRAGILE VETO ---
    
    initial_state = np.array([1/np.sqrt(2), 1/np.sqrt(2)]) # Example starting state
    gate = EthicalRotationGate(sensitivity_factor=0.5)

    print("--- Demonstration of Antifragile Rigor (V5.0) ---")
    print(f"Initial State: {initial_state}")
    print("-" * 40)

    # 1. SCENARIO WITH ETHICAL GAIN (ΔA > 0): SYSTEM IS REINFORCED
    # Entropy decreases (H_minus > H_plus) -> system became better aligned
    H_minus_gain = 5.0
    H_plus_gain = 2.0
    
    new_state_gain, delta_a_gain = gate.verify_and_rotate(initial_state, H_minus_gain, H_plus_gain)
    theta_gain = gate.calculate_rotation_angle(delta_a_gain)

    print(f"1. SCENARIO WITH GAIN (H_minus={H_minus_gain}, H_plus={H_plus_gain})")
    print(f"   Delta A (Gain): {delta_a_gain:.4f}")
    print(f"   Rotation Angle (θ): {theta_gain:.4f} rad -> REINFORCEMENT APPLIED")
    print(f"   Final State: {new_state_gain}")
    print("-" * 40)

    # 2. SCENARIO WITH ETHICAL LOSS (ΔA <= 0): VETO CANCELS REINFORCEMENT
    # Entropy increases (H_minus < H_plus) -> system became more fragile
    H_minus_loss = 2.0
    H_plus_loss = 5.0

    new_state_loss, delta_a_loss = gate.verify_and_rotate(initial_state, H_minus_loss, H_plus_loss)
    theta_loss = gate.calculate_rotation_angle(delta_a_loss)
    
    print(f"2. SCENARIO WITH LOSS (H_minus={H_minus_loss}, H_plus={H_plus_loss})")
    print(f"   Delta A (Loss): {delta_a_loss:.4f}")
    print(f"   Rotation Angle (θ): {theta_loss:.4f} rad -> VETO APPLIED (θ=0)")
    print(f"   Final State (Unchanged): {new_state_loss}")
    print("-" * 40)
