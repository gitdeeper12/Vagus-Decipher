"""Physics constraints for NISSD - Jacobian sign constraints
Equation (8): sign(∂f_θ_i/∂S_j) = C_ij
"""

import numpy as np
from typing import Tuple

class JacobianConstraint:
    """Enforce sign constraints on cytokine coupling matrix"""
    
    # Cytokine coupling sign matrix C_ij (Eq. 8)
    # Rows/Cols: TNF-a, IL-1b, IL-6, IL-10, C3a, NeutAct, CoagAct
    COUPLING_MATRIX = np.array([
        [ 1,  1,  0, -1,  0,  0,  0],  # TNF-a
        [ 1,  1,  0, -1,  0,  0,  0],  # IL-1b
        [ 1,  1,  1,  0,  0,  0,  0],  # IL-6
        [-1,  1,  1,  0,  0,  0,  0],  # IL-10
        [ 0,  0,  0,  0,  1,  1,  0],  # C3a
        [ 0,  0,  0,  0,  1,  1,  0],  # NeutAct
        [ 0,  0,  0,  0,  0,  1, -1]   # CoagAct
    ])
    
    @classmethod
    def compute_jacobian(cls, f_theta, S: np.ndarray, epsilon: float = 1e-5) -> np.ndarray:
        """Compute numerical Jacobian of state transition"""
        n = len(S)
        J = np.zeros((n, n))
        
        for i in range(n):
            S_plus = S.copy()
            S_plus[i] += epsilon
            S_minus = S.copy()
            S_minus[i] -= epsilon
            
            f_plus = f_theta(S_plus)
            f_minus = f_theta(S_minus)
            
            J[:, i] = (f_plus - f_minus) / (2 * epsilon)
        
        return J
    
    @classmethod
    def sign_constraint_loss(cls, J: np.ndarray) -> float:
        """Compute loss for sign constraint violation"""
        loss = 0.0
        n = J.shape[0]
        
        for i in range(n):
            for j in range(n):
                target_sign = np.sign(cls.COUPLING_MATRIX[i, j])
                actual_sign = np.sign(J[i, j])
                
                if target_sign != 0 and actual_sign != target_sign:
                    loss += 1.0
                elif target_sign == 0 and abs(J[i, j]) > 0.01:
                    loss += abs(J[i, j])
        
        return loss / (n * n)
    
    @classmethod
    def enforce_constraints(cls, J: np.ndarray) -> np.ndarray:
        """Project Jacobian onto allowed sign space"""
        J_constrained = J.copy()
        n = J.shape[0]
        
        for i in range(n):
            for j in range(n):
                target_sign = cls.COUPLING_MATRIX[i, j]
                if target_sign > 0:
                    J_constrained[i, j] = max(0, J_constrained[i, j])
                elif target_sign < 0:
                    J_constrained[i, j] = min(0, J_constrained[i, j])
                else:
                    J_constrained[i, j] = 0.0
        
        return J_constrained
