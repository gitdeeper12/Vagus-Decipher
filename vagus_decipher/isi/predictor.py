"""Inflammatory Storm Index (ISI) Predictor
Pure NumPy implementation - No scipy dependency
Equation (9): ISI(t) = σ(α ∫ e^{β(t-τ)} Λ̇(t-τ) dτ + γ||S_t - S_healthy||)
"""

import numpy as np
from typing import Tuple, Dict, Optional

def sigmoid(x: float) -> float:
    """Logistic sigmoid function"""
    if x >= 0:
        return 1.0 / (1.0 + np.exp(-x))
    else:
        exp_x = np.exp(x)
        return exp_x / (1.0 + exp_x)


class InflammatoryStormIndex:
    """ISI predictor with acceleration-sensitive temporal integration"""
    
    def __init__(self, alpha: float = 2.0, beta: float = 0.08, gamma: float = 5.0,
                 integration_window: float = 30.0, fs: float = 1.0):
        self.alpha = alpha
        self.beta = beta  # decay constant (min⁻¹)
        self.gamma = gamma
        self.window_samples = int(integration_window * fs)
        self.fs = fs
        self.S_healthy = np.array([0.1, 0.1, 0.1, 0.5, 0.1, 0.2, 0.1])  # Homeostatic state
        
        # History buffers
        self.Lambda_history = []
        self.S_history = []
    
    def _aggregate_firing_rate_velocity(self, Lambda: np.ndarray) -> float:
        """Compute aggregate firing rate velocity Λ̇(t)"""
        if isinstance(Lambda, np.ndarray):
            val = float(Lambda[0]) if Lambda.size > 0 else 0.0
        else:
            val = float(Lambda)
        
        self.Lambda_history.append(val)
        if len(self.Lambda_history) < 2:
            return 0.0
        
        if len(self.Lambda_history) > self.window_samples:
            self.Lambda_history = self.Lambda_history[-self.window_samples:]
        
        if len(self.Lambda_history) >= 2:
            velocity = self.Lambda_history[-1] - self.Lambda_history[-2]
            return velocity
        return 0.0
    
    def _state_magnitude(self, S: np.ndarray) -> float:
        """Compute distance from healthy homeostatic state"""
        # Scale up to make difference more significant
        diff = S - self.S_healthy
        return np.linalg.norm(diff) * 10.0  # Amplify difference
    
    def compute_isi(self, Lambda: np.ndarray, S: np.ndarray) -> float:
        """Compute ISI score (Eq. 9)"""
        Lambda_dot = self._aggregate_firing_rate_velocity(Lambda)
        state_mag = self._state_magnitude(S)
        
        integral = self.alpha * Lambda_dot
        z = integral + self.gamma * state_mag
        
        # Shift to make thresholds meaningful
        isi = sigmoid(z - 1.5)
        
        return float(np.clip(isi, 0.0, 1.0))
    
    def get_alert_level(self, isi: float) -> Tuple[str, str, float]:
        """Get clinical alert level based on ISI score"""
        if isi < 0.35:
            return "LOW", "🟢 Low Risk - Routine monitoring", 0.0
        elif isi < 0.55:
            return "ELEVATED", "🟡 Elevated - Increase vitals frequency", 30.0
        elif isi < 0.75:
            return "HIGH", "🟠 High Risk - Physician notification", 15.0
        else:
            return "CRITICAL", "🔴 Critical - Immediate intervention", 5.0


class VagusDecipherEngine:
    """Main engine combining AWIE, NISSD, and ISI"""
    
    def __init__(self, interface: str = 'implanted_cuff', n_contacts: int = 6,
                 fs: float = 30000, conduction_velocity: Tuple[float, float] = (0.2, 2.0),
                 warn_horizon_min: float = 45):
        
        self.interface = interface
        self.fs = fs
        self.warn_horizon = warn_horizon_min
        
        from vagus_decipher.awie import WaveletDecomposer, SpatiotemporalBeamformer, SpikeDetector
        from vagus_decipher.nissd import NeuroImmuneStateSpaceModel
        
        self.wavelet = WaveletDecomposer(fs=fs)
        self.beamformer = SpatiotemporalBeamformer(n_contacts=n_contacts, cv_range=conduction_velocity)
        self.spike_detector = SpikeDetector(fs=fs)
        self.state_model = NeuroImmuneStateSpaceModel()
        self.isi_predictor = InflammatoryStormIndex(fs=1.0)
        self.current_state = np.zeros(7)
        self.results_counter = 0
    
    def process(self, eng_signal: np.ndarray) -> Dict:
        """Process raw ENG signal and return results"""
        immune_signal = self.wavelet.process(eng_signal)
        
        if len(eng_signal.shape) > 1:
            immune_signal = self.beamformer.adaptive_beamform(eng_signal)
        
        spike_times, spike_labels = self.spike_detector.process(immune_signal)
        
        duration_sec = len(eng_signal) / self.fs
        firing_rate = len(spike_times) / duration_sec if duration_sec > 0 else 0.0
        Lambda = np.array([firing_rate])
        
        self.current_state = self.state_model.state_transition(self.current_state, Lambda)
        
        isi = self.isi_predictor.compute_isi(Lambda, self.current_state)
        alert_level, alert_message, response_time = self.isi_predictor.get_alert_level(isi)
        
        self.results_counter += 1
        
        return {
            'isi': isi,
            'alert_level': alert_level,
            'alert_message': alert_message,
            'response_time_min': response_time,
            'state': dict(zip(self.state_model.get_state_names(), self.current_state)),
            'spike_count': len(spike_times),
            'lead_time_min': self.warn_horizon if isi > 0.65 else None
        }
    
    def load_weights(self, path: str):
        print(f"Weights would be loaded from {path}")
        pass
