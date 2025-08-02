"""
Core data models for the cervical pose detection system.
"""
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Tuple
import numpy as np


class ExerciseType(Enum):
    """Enumeration of cervical exercise types"""
    CERVICAL_FLEXION = "Cervical Flexion (Chin-to-chest)"
    CERVICAL_EXTENSION = "Cervical Extension (Look upward)"
    LATERAL_NECK_TILT = "Lateral Neck Tilt (Left and Right)"
    NECK_ROTATION = "Neck Rotation (Turn head left/right)"
    CHIN_TUCK = "Chin Tuck (Retract chin)"


class DetectionStatus(Enum):
    """Status of exercise detection"""
    CALIBRATING = "calibrating"
    READY = "ready"
    DETECTED = "detected"
    NOT_DETECTED = "not_detected"
    ERROR = "error"


@dataclass
class LandmarkPoints:
    """Data class to store key landmark points"""
    nose: np.ndarray
    left_ear: np.ndarray
    right_ear: np.ndarray
    left_shoulder: np.ndarray
    right_shoulder: np.ndarray


@dataclass
class ExerciseResult:
    """Data class to store exercise detection results with enhanced feedback"""
    exercise_type: ExerciseType
    detected: bool
    confidence: float
    status: DetectionStatus
    status_message: str = ""
    metrics: Optional[dict] = None
    timestamp: Optional[float] = None
    
    def to_dict(self) -> dict:
        """Convert result to dictionary for serialization"""
        return {
            'exercise_type': self.exercise_type.value,
            'detected': self.detected,
            'confidence': self.confidence,
            'status': self.status.value,
            'status_message': self.status_message,
            'metrics': self.metrics or {},
            'timestamp': self.timestamp
        }


@dataclass
class CalibrationState:
    """Tracks calibration progress for each detector"""
    frames_collected: int = 0
    frames_required: int = 15
    baseline_values: dict = None
    is_complete: bool = False
    
    @property
    def progress_percentage(self) -> float:
        """Get calibration progress as percentage"""
        return min(100.0, (self.frames_collected / self.frames_required) * 100)
    
    def reset(self):
        """Reset calibration state"""
        self.frames_collected = 0
        self.baseline_values = None
        self.is_complete = False


@dataclass
class SystemConfig:
    """Configuration for the detection system"""
    # Detection thresholds
    flexion_threshold: float = 0.85
    extension_threshold: float = 1.15
    tilt_threshold: float = 0.15
    rotation_threshold: float = 1.5
    chin_tuck_threshold: float = 0.8
    
    # Calibration settings
    calibration_frames: int = 15
    confidence_smoothing: float = 0.3
    
    # Performance settings
    min_detection_confidence: float = 0.5
    min_tracking_confidence: float = 0.5
    model_complexity: int = 1
    
    # UI settings
    fps_limit: int = 15
    video_width: int = 640
    video_height: int = 480
