"""Spike detection and sorting for immune-afferent C-fibers
No heavy dependencies - pure numpy implementation
"""

import numpy as np
from typing import Tuple, List

class SpikeDetector:
    """Threshold-based spike detection with simple clustering"""
    
    def __init__(self, threshold_sd: float = 3.5, refractory_ms: float = 1.0, fs: float = 30000):
        self.threshold_sd = threshold_sd
        self.refractory_samples = int(refractory_ms * fs / 1000)
        self.fs = fs
    
    def detect_spikes(self, signal: np.ndarray) -> np.ndarray:
        """Detect spike times using amplitude thresholding"""
        threshold = self.threshold_sd * np.std(signal)
        
        peaks = []
        i = 0
        while i < len(signal):
            if signal[i] > threshold:
                peaks.append(i)
                i += self.refractory_samples
            else:
                i += 1
        
        return np.array(peaks)
    
    def extract_waveforms(self, signal: np.ndarray, spike_times: np.ndarray, 
                          window_ms: float = 2.0) -> np.ndarray:
        """Extract spike waveforms around detected times"""
        window_samples = int(window_ms * self.fs / 1000)
        waveforms = []
        
        for t in spike_times:
            start = max(0, t - window_samples // 2)
            end = min(len(signal), t + window_samples // 2)
            waveform = signal[start:end]
            
            if len(waveform) < window_samples:
                waveform = np.pad(waveform, (0, window_samples - len(waveform)))
            
            waveforms.append(waveform)
        
        return np.array(waveforms) if waveforms else np.array([])
    
    def simple_sort(self, waveforms: np.ndarray, n_clusters: int = 3) -> np.ndarray:
        """Simple amplitude-based clustering (no sklearn)"""
        if len(waveforms) == 0:
            return np.array([])
        
        # Use peak amplitude for clustering
        amplitudes = np.max(waveforms, axis=1) - np.min(waveforms, axis=1)
        
        # Simple threshold-based clustering
        if len(amplitudes) == 0:
            return np.array([])
        
        labels = np.zeros(len(amplitudes), dtype=int)
        threshold = np.percentile(amplitudes, 100 // n_clusters)
        
        for i, amp in enumerate(amplitudes):
            labels[i] = min(int(amp / threshold), n_clusters - 1) if threshold > 0 else 0
        
        return labels
    
    def process(self, signal: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Full spike detection and sorting pipeline"""
        spike_times = self.detect_spikes(signal)
        waveforms = self.extract_waveforms(signal, spike_times)
        
        if len(waveforms) > 0:
            labels = self.simple_sort(waveforms)
        else:
            labels = np.array([])
        
        return spike_times, labels
