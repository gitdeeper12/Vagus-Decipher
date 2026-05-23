"""Unit tests for AWIE module"""

import unittest
import numpy as np
import sys
sys.path.append('../..')

from vagus_decipher.awie import WaveletDecomposer, SpatiotemporalBeamformer, SpikeDetector

class TestAWIE(unittest.TestCase):
    
    def setUp(self):
        self.fs = 30000
        self.duration = 0.1
        self.signal = np.random.randn(int(self.fs * self.duration)) * 0.1
        # Add synthetic spikes
        for _ in range(5):
            pos = np.random.randint(0, len(self.signal))
            if pos + 10 < len(self.signal):
                self.signal[pos:pos+10] += 1.0
    
    def test_wavelet_decomposer(self):
        decomposer = WaveletDecomposer(fs=self.fs)
        result = decomposer.process(self.signal)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), len(self.signal))
    
    def test_beamformer(self):
        beamformer = SpatiotemporalBeamformer(n_contacts=6)
        signals = np.random.randn(6, 1000)
        output = beamformer.adaptive_beamform(signals)
        self.assertIsInstance(output, np.ndarray)
    
    def test_spike_detector(self):
        detector = SpikeDetector(fs=self.fs)
        spikes, labels = detector.process(self.signal)
        self.assertIsInstance(spikes, np.ndarray)
        self.assertIsInstance(labels, np.ndarray)

if __name__ == '__main__':
    unittest.main()
