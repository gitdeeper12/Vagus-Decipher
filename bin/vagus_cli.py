#!/usr/bin/env python3
"""Vagus-Decipher CLI Tool"""

import argparse
import numpy as np
from vagus_decipher import VagusDecipherEngine
from vagus_decipher.utils import generate_synthetic_eng

def main():
    parser = argparse.ArgumentParser(description='Vagus-Decipher AI CLI')
    parser.add_argument('--interface', type=str, default='implanted_cuff',
                        choices=['implanted_cuff', 'acute_hook', 'tavns'])
    parser.add_argument('--duration', type=float, default=10.0, help='Duration in seconds')
    parser.add_argument('--verbose', '-v', action='store_true')
    
    args = parser.parse_args()
    
    print(f"Initializing Vagus-Decipher with {args.interface} interface...")
    engine = VagusDecipherEngine(interface=args.interface)
    
    print(f"Generating synthetic ENG data ({args.duration}s)...")
    signal = generate_synthetic_eng(args.duration, fs=30000)
    
    print("Processing...")
    chunk_size = int(0.1 * 30000)
    results = []
    
    for i in range(0, len(signal), chunk_size):
        chunk = signal[i:i+chunk_size]
        if len(chunk) == chunk_size:
            result = engine.process(chunk)
            results.append(result)
    
    print(f"\nResults:")
    print(f"  Average ISI: {np.mean([r['isi'] for r in results]):.3f}")
    print(f"  Max ISI: {np.max([r['isi'] for r in results]):.3f}")
    
    final_alert = results[-1]['alert_level'] if results else "UNKNOWN"
    print(f"  Final Alert Level: {final_alert}")

if __name__ == '__main__':
    main()
