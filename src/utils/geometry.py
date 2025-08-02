"""
Utility functions for geometric calculations and landmark processing.
"""
import numpy as np
import mediapipe as mp
from typing import Optional, Tuple
from ..core.models import LandmarkPoints


class GeometryUtils:
    """Utility class for geometric calculations"""
    
    @staticmethod
    def calculate_distance(point1: np.ndarray, point2: np.ndarray) -> float:
        """Calculate Euclidean distance between two points"""
        return np.linalg.norm(point1 - point2)
    
    @staticmethod
    def calculate_angle(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> float:
        """Calculate angle formed by three points (p1-p2-p3)"""
        v1 = p1 - p2
        v2 = p3 - p2
        
        # Avoid division by zero
        norm1, norm2 = np.linalg.norm(v1), np.linalg.norm(v2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        cos_angle = np.dot(v1, v2) / (norm1 * norm2)
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        return np.arccos(cos_angle) * 180 / np.pi
    
    @staticmethod
    def calculate_ratio(distance: float, baseline: float) -> float:
        """Calculate ratio with baseline, handling edge cases"""
        if baseline == 0:
            return 1.0
        return distance / baseline
    
    @staticmethod
    def smooth_value(current: float, previous: float, smoothing_factor: float = 0.3) -> float:
        """Apply exponential smoothing to a value"""
        return smoothing_factor * current + (1 - smoothing_factor) * previous


class LandmarkExtractor:
    """Class responsible for extracting key landmarks from MediaPipe results"""
    
    @staticmethod
    def extract_landmarks(pose_results, frame_shape) -> Optional[LandmarkPoints]:
        """Extract key landmarks from MediaPipe pose results"""
        if not pose_results.pose_landmarks:
            return None
        
        landmarks = pose_results.pose_landmarks.landmark
        h, w = frame_shape[:2]
        
        try:
            # MediaPipe landmark indices
            # 0: nose, 7: left_ear, 8: right_ear, 11: left_shoulder, 12: right_shoulder
            return LandmarkPoints(
                nose=np.array([landmarks[0].x * w, landmarks[0].y * h]),
                left_ear=np.array([landmarks[7].x * w, landmarks[7].y * h]),
                right_ear=np.array([landmarks[8].x * w, landmarks[8].y * h]),
                left_shoulder=np.array([landmarks[11].x * w, landmarks[11].y * h]),
                right_shoulder=np.array([landmarks[12].x * w, landmarks[12].y * h])
            )
        except (IndexError, AttributeError) as e:
            # Handle missing landmarks gracefully
            return None
    
    @staticmethod
    def is_pose_visible(landmarks: LandmarkPoints, min_visibility: float = 0.5) -> bool:
        """Check if the pose landmarks are sufficiently visible"""
        # This is a simple check - in a more advanced system,
        # you could check actual visibility scores from MediaPipe
        try:
            # Check if all landmarks are within reasonable bounds
            for point in [landmarks.nose, landmarks.left_ear, landmarks.right_ear, 
                         landmarks.left_shoulder, landmarks.right_shoulder]:
                if np.any(point < 0) or np.any(np.isnan(point)):
                    return False
            return True
        except:
            return False


class MathUtils:
    """Mathematical utility functions"""
    
    @staticmethod
    def normalize_angle(angle: float) -> float:
        """Normalize angle to 0-360 range"""
        return angle % 360
    
    @staticmethod
    def clamp(value: float, min_val: float, max_val: float) -> float:
        """Clamp value to specified range"""
        return max(min_val, min(max_val, value))
    
    @staticmethod
    def map_range(value: float, from_min: float, from_max: float, 
                  to_min: float, to_max: float) -> float:
        """Map value from one range to another"""
        if from_max == from_min:
            return to_min
        
        ratio = (value - from_min) / (from_max - from_min)
        return to_min + ratio * (to_max - to_min)
