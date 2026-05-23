"""Benchmark M2: Sterile SIRS Validation"""

import numpy as np
from vagus_decipher import VagusDecipherEngine

def run_sirs_benchmark():
    """Run sterile SIRS validation benchmark"""
    print("=" * 60)
    print("M2: Sterile SIRS Benchmark")
    print("=" * 60)
    
    engine = VagusDecipherEngine(interface='implanted_cuff')
    
    # Simulated SIRS response (simplified)
    times = np.arange(0, 180, 1)
    isi_scores = []
    
    for t in times:
        if t < 15:
            Lambda = np.array([8.0])
            S = np.array([0.15, 0.15, 0.12, 0.55, 0.12, 0.25, 0.12])
        elif t < 45:
            Lambda = np.array([20.0])
            S = np.array([0.4, 0.4, 0.3, 0.45, 0.3, 0.4, 0.25])
        else:
            Lambda = np.array([45.0])
            S = np.array([0.8, 0.8, 0.7, 0.25, 0.6, 0.7, 0.45])
        
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
    run_sirs_benchmark()
