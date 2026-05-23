"""Clinical alert thresholds for ISI"""

from enum import Enum
from typing import Tuple

class AlertLevel(Enum):
    """Clinical alert levels based on ISI score"""
    LOW = (0.0, 0.35, "🟢 Low Risk", "Routine monitoring", 0)
    ELEVATED = (0.35, 0.55, "🟡 Elevated", "Increase vital signs frequency", 30)
    HIGH = (0.55, 0.75, "🟠 High Risk", "Physician notification + lab panel", 15)
    CRITICAL = (0.75, 1.0, "🔴 Critical", "Immediate intervention protocol", 5)


class ClinicalThresholds:
    """Clinical threshold configuration"""
    
    # Default thresholds (calibrated on M1 LPS validation set)
    DEFAULT_THRESHOLDS = {
        'low': 0.35,
        'elevated': 0.55,
        'high': 0.75,
        'critical': 0.90
    }
    
    @classmethod
    def get_alert_level(cls, isi: float) -> Tuple[AlertLevel, str, float]:
        """Get alert level for given ISI score"""
        for level in AlertLevel:
            if level.value[0] <= isi < level.value[1]:
                return level, level.value[2], level.value[4]
        
        if isi >= AlertLevel.CRITICAL.value[0]:
            return AlertLevel.CRITICAL, AlertLevel.CRITICAL.value[2], AlertLevel.CRITICAL.value[4]
        
        return AlertLevel.LOW, AlertLevel.LOW.value[2], AlertLevel.LOW.value[4]
    
    @classmethod
    def get_response_time(cls, isi: float) -> float:
        """Get recommended response time in minutes"""
        level, _, response_time = cls.get_alert_level(isi)
        return response_time
    
    @classmethod
    def is_alert(cls, isi: float) -> bool:
        """Check if ISI exceeds alert threshold"""
        return isi >= cls.DEFAULT_THRESHOLDS['elevated']
