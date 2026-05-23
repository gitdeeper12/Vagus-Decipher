"""Benchmark M3: CAR-T CRS Analog Validation"""

import numpy as np
from vagus_decipher import VagusDecipherEngine

def run_cart_benchmark():
    """Run CAR-T CRS validation benchmark"""
    print("=" * 60)
    print("M3: CAR-T CRS Analog Benchmark")
    print("=" * 60)
    
    engine = VagusDecipherEngine(interface='implanted_cuff')
    
    # Simulated CAR-T CRS response (simplified)
    times = np.arange(0, 180, 1)
    isi_scores = []
    
    for t in times:
        if t < 20:
            Lambda = np.array([6.0])
            S = np.array([0.12, 0.12, 0.11, 0.52, 0.11, 0.22, 0.11])
        elif t < 50:
            Lambda = np.array([25.0])
            S = np.array([0.5, 0.5, 0.35, 0.42, 0.35, 0.45, 0.3])
        else:
            Lambda = np.array([55.0])
            S = np.array([0.95, 0.95, 0.85, 0.15, 0.75, 0.85, 0.55])
        
        isi = engine.isi_predictor.compute_isi(Lambda, S)
        isi_scores.append(isi)
    
    # Find alert time
    alert_time = None
    for i, isi in enumerate(isi_scores):
        if isi > 0.65 and alert_time is None:
            alert_time = times[i]
            break
    
    print(f"Alert triggered at t = {alert_time} minutes")
    print(f"Final ISI: {isi_scores[-1]:.3f}")
    
    return {'alert_time': alert_time, 'final_isi': isi_scores[-1]}

if __name__ == '__main__':
    run_cart_benchmark()
