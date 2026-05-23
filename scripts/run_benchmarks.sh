#!/bin/bash

echo "=========================================="
echo "Running Vagus-Decipher Benchmarks"
echo "=========================================="

echo ""
echo "M1: LPS Endotoxemia"
python benchmarks/m1_lps_endotoxemia.py

echo ""
echo "M2: Sterile SIRS"
python benchmarks/m2_sterile_sirs.py

echo ""
echo "M3: CAR-T CRS"
python benchmarks/m3_car_t_crs.py

echo ""
echo "All benchmarks completed."
