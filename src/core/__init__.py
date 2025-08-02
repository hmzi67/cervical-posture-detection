"""
Core detection system components.
"""

from .detection_system import ExerciseDetectionSystem
from .models import ExerciseType, DetectionStatus, LandmarkPoints, ExerciseResult, SystemConfig
from .video_processor import VideoProcessor

__all__ = [
    'ExerciseDetectionSystem',
    'VideoProcessor',
    'ExerciseType',
    'DetectionStatus',
    'LandmarkPoints',
    'ExerciseResult',
    'SystemConfig'
]
