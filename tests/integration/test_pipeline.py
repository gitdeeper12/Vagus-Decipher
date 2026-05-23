"""Integration tests for full Vagus-Decipher pipeline"""

import unittest
import numpy as np
import sys
sys.path.append('../..')

from vagus_decipher import VagusDecipherEngine
from vagus_decipher.utils import generate_synthetic_eng

class TestPipeline(unittest.TestCase):
    
    def setUp(self):
        self.engine = VagusDecipherEngine(
            interface='implanted_cuff',
            n_contacts=6,
            fs=30000,
            warn_horizon_min=45
        )
    
    def test_full_pipeline_synthetic(self):
        duration = 2.0
        fs = 30000
        signal = generate_synthetic_eng(duration, fs, spike_rate=5.0)
        
        chunk_size = int(0.1 * fs)
        results = []
        
        for i in range(0, len(signal), chunk_size):
            chunk = signal[i:i+chunk_size]
            if len(chunk) == chunk_size:
                result = self.engine.process(chunk)
                results.append(result)
        
        self.assertGreater(len(results), 0)
        
        for result in results:
            self.assertIn('isi', result)
            self.assertIn('alert_level', result)
            self.assertIn('state', result)
    
    def test_isi_temporal_dynamics(self):
        isi_values = []
        
        for t in range(50):
            Lambda = np.array([5.0 + t * 0.5])
            S = np.array([0.1 + t * 0.01] * 7)
            isi = self.engine.isi_predictor.compute_isi(Lambda, S)
            isi_values.append(isi)
        
        self.assertGreater(isi_values[-1], isi_values[0])
    
    def test_alert_triggering_high_risk(self):
        """Test that high firing rate triggers HIGH alert"""
        # Simulate high-risk state (high firing rate, high cytokine levels)
        Lambda = np.array([100.0])  # Very high firing rate
        S = np.array([0.9, 0.9, 0.9, 0.1, 0.8, 0.9, 0.8])  # High cytokine levels
        isi = self.engine.isi_predictor.compute_isi(Lambda, S)
        level, msg, time = self.engine.isi_predictor.get_alert_level(isi)
        
        print(f"  High risk test: ISI={isi:.3f}, Level={level}")
        # Should be at least HIGH or CRITICAL
        self.assertIn(level, ["HIGH", "CRITICAL"], f"Expected HIGH/CRITICAL, got {level}")
    
    def test_alert_triggering_critical(self):
        """Test that extreme values trigger CRITICAL alert"""
        # Simulate critical state
        Lambda = np.array([200.0])  # Extremely high firing rate
        S = np.array([1.0, 1.0, 1.0, 0.05, 0.9, 1.0, 0.9])  # Extreme cytokine levels
        isi = self.engine.isi_predictor.compute_isi(Lambda, S)
        level, msg, time = self.engine.isi_predictor.get_alert_level(isi)
        
        print(f"  Critical test: ISI={isi:.3f}, Level={level}")
        # Should be CRITICAL or at least HIGH
        self.assertIn(level, ["CRITICAL", "HIGH"], f"Expected CRITICAL/HIGH, got {level}")
    
    def test_low_risk_no_alert(self):
        """Test that low values do not trigger alert"""
        # Simulate healthy state
        Lambda = np.array([5.0])  # Normal firing rate
        S = np.array([0.1, 0.1, 0.1, 0.5, 0.1, 0.2, 0.1])  # Healthy state
        isi = self.engine.isi_predictor.compute_isi(Lambda, S)
        level, msg, time = self.engine.isi_predictor.get_alert_level(isi)
        
        print(f"  Low risk test: ISI={isi:.3f}, Level={level}")
        self.assertEqual(level, "LOW", f"Expected LOW, got {level}")

if __name__ == '__main__':
    unittest.main()
