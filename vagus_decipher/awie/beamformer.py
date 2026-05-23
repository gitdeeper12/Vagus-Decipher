"""Spatiotemporal beamformer for interference rejection
Equation (4): y(t) = Σ w_k · x_k(t - τ_k(v_C))
"""

import numpy as np
from typing import Tuple, Optional

class SpatiotemporalBeamformer:
    """C-fiber velocity-tuned beamformer"""
    
    def __init__(self, n_contacts: int = 6, spacing_mm: float = 2.0, 
                 cv_range: Tuple[float, float] = (0.2, 2.0)):
        self.n_contacts = n_contacts
        self.spacing = spacing_mm / 1000  # Convert to meters
        self.cv_min, self.cv_max = cv_range
        self.weights = np.ones(n_contacts) / n_contacts
    
    def compute_steering_delays(self, conduction_velocity: float) -> np.ndarray:
        """Compute steering delays for target conduction velocity"""
        delays = np.arange(self.n_contacts) * self.spacing / conduction_velocity
        return delays
    
    def beamform(self, signals: np.ndarray, conduction_velocity: float) -> np.ndarray:
        """Apply beamformer to multi-contact signals (Eq. 4)"""
        delays = self.compute_steering_delays(conduction_velocity)
        
        # Convert delays to samples
        fs = 30000  # Default sampling rate
        delay_samples = np.round(delays * fs).astype(int)
        
        output = np.zeros(signals.shape[1])
        for k in range(self.n_contacts):
            if delay_samples[k] < signals.shape[1]:
                shifted = np.roll(signals[k, :], delay_samples[k])
                output += self.weights[k] * shifted
        
        return output
    
    def adaptive_beamform(self, signals: np.ndarray) -> np.ndarray:
        """Adaptive beamforming across C-fiber velocity range"""
        best_output = None
        best_cv = self.cv_min
        
        for cv in np.linspace(self.cv_min, self.cv_max, 20):
            output = self.beamform(signals, cv)
            power = np.sum(output**2)
            
            if best_output is None or power > np.sum(best_output**2):
                best_output = output
                best_cv = cv
        
        return best_output
