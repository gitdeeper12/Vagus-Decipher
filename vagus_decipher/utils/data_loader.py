"""Data loading utilities for ENG and cytokine data
Pure python CSV parsing - no pandas dependency
"""

import numpy as np
from typing import Tuple, Dict, Optional

def load_csv_data(filepath: str) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
    """Load CSV data without pandas"""
    data = {}
    headers = []
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    if not lines:
        return np.array([]), {}
    
    # Parse headers
    headers = lines[0].strip().split(',')
    
    # Parse data
    numeric_data = {h: [] for h in headers}
    
    for line in lines[1:]:
        if line.strip():
            values = line.strip().split(',')
            for i, header in enumerate(headers):
                if i < len(values):
                    try:
                        numeric_data[header].append(float(values[i]))
                    except ValueError:
                        numeric_data[header].append(0.0)
    
    # Convert to numpy arrays
    for h in headers:
        numeric_data[h] = np.array(numeric_data[h])
    
    # Extract time column if exists
    time = numeric_data.get('time_min', numeric_data.get('time', np.array([])))
    
    return time, numeric_data

def load_eng_data(filepath: str, fs: float = 30000) -> Tuple[np.ndarray, np.ndarray]:
    """Load ENG recording data from CSV"""
    time, data = load_csv_data(filepath)
    
    # Find signal columns (all numeric columns except time)
    signal_cols = [k for k in data.keys() if k not in ['time_min', 'time', 'ISI', 'alert_level']]
    
    if signal_cols:
        signals = np.array([data[col] for col in signal_cols])
    else:
        signals = np.array([])
    
    return time, signals

def load_cytokine_data(filepath: str) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
    """Load cytokine concentration data"""
    time, data = load_csv_data(filepath)
    return time, data

def generate_synthetic_eng(duration: float, fs: float = 30000, 
                           spike_rate: float = 5.0) -> np.ndarray:
    """Generate synthetic ENG signal for testing"""
    t = np.arange(0, duration, 1/fs)
    
    # Initialize signal
    signal = np.random.randn(len(t)) * 0.1
    
    # Generate spike times
    n_spikes = int(spike_rate * duration)
    spike_times = np.random.exponential(1/spike_rate, n_spikes)
    spike_times = np.cumsum(spike_times)
    spike_times = spike_times[spike_times < duration]
    
    # Spike waveform (simple)
    def spike_waveform(tau):
        return tau * np.exp(-tau**2 / (2 * 0.001**2))
    
    for spike_time in spike_times:
        idx = int(spike_time * fs)
        if idx < len(t):
            tau = t - spike_time
            window = np.where(np.abs(tau) < 0.005)[0]
            if len(window) > 0:
                signal[window] += spike_waveform(tau[window])
    
    return signal
