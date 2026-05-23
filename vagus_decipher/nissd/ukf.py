"""Unscented Kalman Filter (UKF) for non-Gaussian state estimation"""

import numpy as np
from typing import Tuple, Callable

class UnscentedKalmanFilter:
    """UKF implementation for NISSD state estimation"""
    
    def __init__(self, state_dim: int, meas_dim: int, alpha: float = 0.01, 
                 beta: float = 2.0, kappa: float = 0.0):
        self.n = state_dim
        self.m = meas_dim
        self.alpha = alpha
        self.beta = beta
        self.kappa = kappa
        
        # Sigma point parameters
        self.lambda_ = alpha**2 * (self.n + kappa) - self.n
        self.Wm, self.Wc = self._compute_weights()
        
        # State and covariance
        self.x = np.zeros(state_dim)
        self.P = np.eye(state_dim) * 0.1
    
    def _compute_weights(self) -> Tuple[np.ndarray, np.ndarray]:
        """Compute sigma point weights"""
        n = self.n
        lambda_ = self.lambda_
        
        Wm = np.zeros(2*n + 1)
        Wc = np.zeros(2*n + 1)
        
        Wm[0] = lambda_ / (n + lambda_)
        Wc[0] = Wm[0] + (1 - self.alpha**2 + self.beta)
        
        for i in range(1, 2*n + 1):
            Wm[i] = 1 / (2 * (n + lambda_))
            Wc[i] = Wm[i]
        
        return Wm, Wc
    
    def _generate_sigma_points(self) -> np.ndarray:
        """Generate sigma points around current state"""
        n = self.n
        lambda_ = self.lambda_
        
        sqrt_P = np.linalg.cholesky((n + lambda_) * self.P)
        
        sigma_points = np.zeros((2*n + 1, n))
        sigma_points[0] = self.x
        
        for i in range(n):
            sigma_points[i + 1] = self.x + sqrt_P[i]
            sigma_points[n + i + 1] = self.x - sqrt_P[i]
        
        return sigma_points
    
    def predict(self, f: Callable[[np.ndarray], np.ndarray], dt: float = 0.001):
        """UKF prediction step"""
        sigma_points = self._generate_sigma_points()
        
        # Transform sigma points through dynamics
        transformed = np.array([f(sigma_points[i], dt) for i in range(len(sigma_points))])
        
        # Predicted mean
        self.x = np.sum(self.Wm[:, np.newaxis] * transformed, axis=0)
        
        # Predicted covariance
        self.P = np.zeros((self.n, self.n))
        for i in range(len(transformed)):
            diff = transformed[i] - self.x
            self.P += self.Wc[i] * np.outer(diff, diff)
        
        return self.x, self.P
    
    def update(self, z: np.ndarray, h: Callable[[np.ndarray], np.ndarray]):
        """UKF update step with measurement"""
        sigma_points = self._generate_sigma_points()
        
        # Transform sigma points through measurement function
        transformed = np.array([h(sigma_points[i]) for i in range(len(sigma_points))])
        
        # Predicted measurement mean
        z_pred = np.sum(self.Wm[:, np.newaxis] * transformed, axis=0)
        
        # Innovation covariance
        Pzz = np.zeros((self.m, self.m))
        Pxz = np.zeros((self.n, self.m))
        
        for i in range(len(transformed)):
            diff_z = transformed[i] - z_pred
            Pzz += self.Wc[i] * np.outer(diff_z, diff_z)
            
            diff_x = sigma_points[i] - self.x
            Pxz += self.Wc[i] * np.outer(diff_x, diff_z)
        
        # Add measurement noise
        Pzz += np.eye(self.m) * 0.05
        
        # Kalman gain
        K = Pxz @ np.linalg.inv(Pzz)
        
        # State update
        innovation = z - z_pred
        self.x = self.x + K @ innovation
        
        # Covariance update
        self.P = self.P - K @ Pzz @ K.T
        
        return self.x, self.P
