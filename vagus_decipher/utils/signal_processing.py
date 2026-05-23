"""Signal processing utilities for ENG data
Pure numpy implementation - no scipy dependency
"""

import numpy as np

def bandpass_filter(x: np.ndarray, fs: float, f_low: float, f_high: float, order: int = 2) -> np.ndarray:
    """Simple FIR bandpass filter using window method"""
    # Simple moving difference as approximation
    # For real applications, use scipy.signal when available
    dt = 1.0 / fs
    
    # Very simple high-pass (remove DC)
    x_hp = x - np.mean(x)
    
    # Simple low-pass (moving average)
    window_size = int(fs / f_high)
    if window_size > 1:
        kernel = np.ones(window_size) / window_size
        x_lp = np.convolve(x_hp, kernel, mode='same')
    else:
        x_lp = x_hp
    
    return x_lp

def notch_filter(x: np.ndarray, fs: float, freq: float = 60.0) -> np.ndarray:
    """Simple notch filter for line noise"""
    # Simple moving average notch
    period = int(fs / freq)
    if period > 1:
        kernel = np.ones(period) / period
        return np.convolve(x, kernel, mode='same')
    return x

def moving_average(x: np.ndarray, window: int) -> np.ndarray:
    """Apply moving average filter"""
    if window <= 1:
        return x.copy()
    kernel = np.ones(window) / window
    return np.convolve(x, kernel, mode='same')
