"""Unit tests for ISI module"""

import unittest
import numpy as np
import sys
sys.path.append('../..')

from vagus_decipher.isi import InflammatoryStormIndex, ClinicalThresholds, VagusDecipherEngine

class TestISI(unittest.TestCase):
    
    def setUp(self):
        self.isi_predictor = InflammatoryStormIndex(fs=1.0)
        self.engine = VagusDecipherEngine()
    
    def test_isi_computation(self):
        Lambda = np.array([10.0])
        S = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
        isi = self.isi_predictor.compute_isi(Lambda, S)
        self.assertGreaterEqual(isi, 0)
        self.assertLessEqual(isi, 1)
    
    def test_alert_levels(self):
        level, msg, time = self.isi_predictor.get_alert_level(0.2)
        self.assertEqual(level, "LOW")
        
        level, msg, time = self.isi_predictor.get_alert_level(0.45)
        self.assertEqual(level, "ELEVATED")
        
        level, msg, time = self.isi_predictor.get_alert_level(0.65)
        self.assertEqual(level, "HIGH")
        
        level, msg, time = self.isi_predictor.get_alert_level(0.85)
        self.assertEqual(level, "CRITICAL")
    
    def test_clinical_thresholds(self):
        self.assertTrue(ClinicalThresholds.is_alert(0.65))
        self.assertFalse(ClinicalThresholds.is_alert(0.2))
        level, msg, time = ClinicalThresholds.get_alert_level(0.65)
        self.assertEqual(time, 15.0)
    
    def test_engine_process(self):
        signal = np.random.randn(30000)
        result = self.engine.process(signal)
        self.assertIn('isi', result)
        self.assertIn('alert_level', result)
        self.assertIn('state', result)
        self.assertIn('spike_count', result)

if __name__ == '__main__':
    unittest.main()
