"""Morlet wavelet decomposition for immune-afferent signal isolation
Pure NumPy implementation - No pywt dependency
Equations: (2) Continuous Wavelet Transform, (3) Immune-Afferent Band Isolation
"""

import numpy as np
from typing import Tuple, Optional

class WaveletDecomposer:
    """Morlet wavelet decomposition for C-fiber signal extraction (Pure NumPy)"""
    
    def __init__(self, fs: float = 30000, f_min: float = 300, f_max: float = 3000, sigma: float = 6.0):
        self.fs = fs
        self.f_min = f_min
        self.f_max = f_max
        self.sigma = sigma
        
        # Calculate scale bounds
        self.a_min = fs / (2 * f_max)
        self.a_max = fs / (2 * f_min)
        self.n_scales = 32  # Reduced for speed
    
    def _morlet_wavelet(self, t: np.ndarray, scale: float) -> np.ndarray:
        """Morlet wavelet function (Eq. 2)"""
        # Normalized time
        tau = t / scale
        # Morlet wavelet: complex exponential * Gaussian envelope
        wavelet = np.exp(-tau**2 / (2 * self.sigma**2)) * np.cos(2 * np.pi * tau)
        return wavelet / np.sqrt(scale)  # Energy normalization
    
    def continuous_wavelet_transform(self, x: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Compute CWT using Morlet wavelet (Eq. 2) - Pure NumPy"""
        n = len(x)
        scales = np.logspace(np.log10(self.a_min), np.log10(self.a_max), self.n_scales)
        coefficients = np.zeros((len(scales), n), dtype=np.float64)
        
        # Compute CWT for each scale
        for i, scale in enumerate(scales):
            # Wavelet length (5 standard deviations)
            w_length = int(5 * scale * self.sigma * self.fs)
            w_length = min(w_length, n // 2)
            
            if w_length > 2:
                t = np.arange(-w_length, w_length + 1) / self.fs
                wavelet = self._morlet_wavelet(t, scale)
                
                # Convolution using FFT
                Xf = np.fft.rfft(x)
                Wf = np.fft.rfft(wavelet, n=n)
                conv = np.fft.irfft(Xf * np.conj(Wf))
                
                coefficients[i, :] = conv[:n]
            else:
                # Simplified for small scales
                coefficients[i, :] = x
        
        return coefficients, scales
    
    def isolate_immune_band(self, coefficients: np.ndarray, scales: np.ndarray) -> np.ndarray:
        """Isolate immune-afferent frequency band (Eq. 3)"""
        # Find indices within immune band
        immune_indices = np.where((scales >= self.a_min) & (scales <= self.a_max))[0]
        
        if len(immune_indices) == 0:
            return np.zeros(coefficients.shape[1])
        
        # Integrate over immune band (sum of coefficients)
        immune_signal = np.sum(coefficients[immune_indices, :], axis=0)
        
        # Normalize
        if np.max(np.abs(immune_signal)) > 0:
            immune_signal = immune_signal / np.max(np.abs(immune_signal))
        
        return immune_signal
    
    def process(self, x: np.ndarray) -> np.ndarray:
        """Full AWIE processing pipeline"""
        coeffs, scales = self.continuous_wavelet_transform(x)
        immune_signal = self.isolate_immune_band(coeffs, scales)
        return immune_signal


def morlet_wavelet(t: np.ndarray, sigma: float = 6.0) -> np.ndarray:
    """Morlet wavelet function (mother wavelet)"""
    return np.exp(-t**2 / (2 * sigma**2)) * np.cos(2 * np.pi * t)
