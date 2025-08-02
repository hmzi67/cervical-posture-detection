"""
Cervical Pose Detection System

A comprehensive system for detecting and analyzing cervical exercises
using computer vision and pose estimation.
"""

__version__ = "1.0.0"
__author__ = "Cervical Pose Detection Team"

# Make core components easily accessible
from .core.detection_system import ExerciseDetectionSystem
from .core.video_processor import VideoProcessor
from .core.models import (
    ExerciseType,
    DetectionStatus,
    LandmarkPoints,
    ExerciseResult,
    SystemConfig
)
from .utils.geometry import GeometryUtils, LandmarkExtractor
from .ui.components import UIComponents, SessionManager

__all__ = [
    'ExerciseDetectionSystem',
    'VideoProcessor',
    'ExerciseType',
    'DetectionStatus',
    'LandmarkPoints',
    'ExerciseResult',
    'SystemConfig',
    'GeometryUtils',
    'LandmarkExtractor',
    'UIComponents',
    'SessionManager'
]
