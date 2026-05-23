"""Neuro-Immune State-Space Model (NISSM)
Pure NumPy implementation - No PyTorch dependency
Equation (7): S_{t+1} = f_θ(S_t) + G_θ·Λ(t) + w_t, Λ(t) = h_φ(S_t) + v_t
"""

import numpy as np
from typing import Tuple, Optional

class NeuralODE:
    """Simple neural ODE using NumPy (no PyTorch)"""
    
    def __init__(self, state_dim: int = 7, hidden_dim: int = 64):
        self.state_dim = state_dim
        self.hidden_dim = hidden_dim
        
        # Initialize weights (Xavier-like initialization)
        self.W1 = np.random.randn(state_dim, hidden_dim) * np.sqrt(2.0 / state_dim)
        self.b1 = np.zeros(hidden_dim)
        self.W2 = np.random.randn(hidden_dim, hidden_dim) * np.sqrt(2.0 / hidden_dim)
        self.b2 = np.zeros(hidden_dim)
        self.W3 = np.random.randn(hidden_dim, state_dim) * np.sqrt(2.0 / hidden_dim)
        self.b3 = np.zeros(state_dim)
    
    def softplus(self, x: np.ndarray) -> np.ndarray:
        """Softplus activation (smooth ReLU)"""
        return np.log(1 + np.exp(np.clip(x, -50, 50)))
    
    def forward(self, S: np.ndarray) -> np.ndarray:
        """Forward pass through neural network"""
        h1 = self.softplus(S @ self.W1 + self.b1)
        h2 = self.softplus(h1 @ self.W2 + self.b2)
        output = self.softplus(h2 @ self.W3 + self.b3)
        return output
    
    def __call__(self, S: np.ndarray) -> np.ndarray:
        return self.forward(S)


class NeuroImmuneStateSpaceModel:
    """NISSM with neural ODE and UKF (Pure NumPy)"""
    
    def __init__(self, state_dim: int = 7, hidden_dim: int = 64):
        self.state_dim = state_dim
        self.f_theta = NeuralODE(state_dim, hidden_dim)
        # G_theta: shape (state_dim, 1) for single firing rate input
        self.G_theta = np.random.randn(state_dim, 1) * 0.01
        self.Q = np.eye(state_dim) * 0.01  # Process noise
        self.R = np.eye(state_dim) * 0.05   # Observation noise
        
        # State component names
        self.state_names = ['TNF_a', 'IL_1b', 'IL_6', 'IL_10', 'C3a', 'NeutAct', 'CoagAct']
    
    def state_transition(self, S: np.ndarray, Lambda: np.ndarray, dt: float = 0.001) -> np.ndarray:
        """Apply state transition (Eq. 7 - State Equation)"""
        # Ensure Lambda is 1D
        if Lambda.ndim > 1:
            Lambda = Lambda.flatten()
        
        # Ensure Lambda has correct dimension for matrix multiplication
        # G_theta is (state_dim, 1), Lambda should be (1,)
        dS = self.f_theta(S)
        Lambda_term = self.G_theta @ Lambda  # Shape: (state_dim,)
        S_next = S + dS * dt + Lambda_term * dt
        S_next = np.maximum(S_next, 0)  # Enforce non-negativity
        return S_next
    
    def observation(self, S: np.ndarray) -> np.ndarray:
        """Predict firing rate from state (Eq. 7 - Observation Equation)"""
        # Simplified: linear mapping from state to firing rate (scalar)
        firing_rate = np.sum(S[:self.state_dim] * 10.0)
        return np.array([firing_rate])
    
    def get_state_names(self) -> list:
        return self.state_names
