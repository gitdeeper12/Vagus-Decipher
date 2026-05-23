"""Vagus-Decipher AI: Neural Decoding of Vagus Nerve Electrophysiology for Real-Time Prediction of Systemic Inflammatory Storms

BIO-MED-02 · Biomedical & Clinical AI Research Series
"""

__version__ = "1.0.0"
__author__ = "Samir Baladi"
__license__ = "MIT"
__doi__ = "10.5281/zenodo.20347323"
__series__ = "BIO-MED-02"

from vagus_decipher.awie import WaveletDecomposer, SpatiotemporalBeamformer, SpikeDetector
from vagus_decipher.nissd import NeuroImmuneStateSpaceModel, UnscentedKalmanFilter
from vagus_decipher.isi import InflammatoryStormIndex, ClinicalThresholds, VagusDecipherEngine

__all__ = [
    "WaveletDecomposer", 
    "SpatiotemporalBeamformer", 
    "SpikeDetector",
    "NeuroImmuneStateSpaceModel", 
    "UnscentedKalmanFilter",
    "InflammatoryStormIndex", 
    "ClinicalThresholds", 
    "VagusDecipherEngine"
]
