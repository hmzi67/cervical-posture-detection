"""
Main detection system that coordinates all exercise detectors.
"""
from typing import Dict, Tuple, List, Optional
import time
from abc import ABC, abstractmethod
import numpy as np

from .models import ExerciseType, ExerciseResult, DetectionStatus, SystemConfig, LandmarkPoints
from ..utils.geometry import LandmarkExtractor, GeometryUtils


class BaseDetector(ABC):
    """Base exercise detector"""
    
    def __init__(self, exercise_type: ExerciseType, config: SystemConfig = None):
        self.exercise_type = exercise_type
        self.config = config or SystemConfig()
        self.calibration_frames = 15
        self.frames_collected = 0
        self.is_calibrated = False
        self.previous_confidence = 0.0
    
    def detect(self, landmarks: LandmarkPoints) -> ExerciseResult:
        if landmarks is None:
            return ExerciseResult(
                self.exercise_type, False, 0.0, DetectionStatus.ERROR,
                "No pose detected - ensure you're visible to camera"
            )
        
        # Handle calibration
        if not self.is_calibrated:
            return self._handle_calibration(landmarks)
        
        # Perform detection
        try:
            detected, confidence, metrics = self._detect_exercise(landmarks)
            
            # Smooth confidence
            smoothed_confidence = GeometryUtils.smooth_value(confidence, self.previous_confidence)
            self.previous_confidence = smoothed_confidence
            
            status_message = self._generate_status_message(detected, smoothed_confidence, metrics)
            
            return ExerciseResult(
                self.exercise_type, detected, smoothed_confidence,
                DetectionStatus.DETECTED if detected else DetectionStatus.NOT_DETECTED,
                status_message, metrics
            )
        except Exception as e:
            return ExerciseResult(
                self.exercise_type, False, 0.0, DetectionStatus.ERROR,
                f"Detection error: {str(e)}"
            )
    
    def _handle_calibration(self, landmarks: LandmarkPoints) -> ExerciseResult:
        self.frames_collected += 1
        self._collect_baseline_data(landmarks)
        
        if self.frames_collected >= self.calibration_frames:
            self._finalize_calibration()
            self.is_calibrated = True
            return ExerciseResult(
                self.exercise_type, False, 0.0, DetectionStatus.READY,
                "✅ Calibration complete! Start exercising now."
            )
        
        progress = (self.frames_collected / self.calibration_frames) * 100
        return ExerciseResult(
            self.exercise_type, False, 0.0, DetectionStatus.CALIBRATING,
            f"🔄 Calibrating... {progress:.0f}% ({self.frames_collected}/{self.calibration_frames})"
        )
    
    @abstractmethod
    def _collect_baseline_data(self, landmarks: LandmarkPoints):
        pass
    
    @abstractmethod
    def _finalize_calibration(self):
        pass
    
    @abstractmethod
    def _detect_exercise(self, landmarks: LandmarkPoints) -> Tuple[bool, float, dict]:
        pass
    
    @abstractmethod
    def _generate_status_message(self, detected: bool, confidence: float, metrics: dict) -> str:
        pass
    
    def reset(self):
        self.frames_collected = 0
        self.is_calibrated = False
        self.previous_confidence = 0.0


class CervicalFlexionDetector(BaseDetector):
    """Cervical flexion detector"""
    
    def __init__(self, config: SystemConfig = None):
        super().__init__(ExerciseType.CERVICAL_FLEXION, config)
        self.baseline_distance = None
        self.calibration_distances = []
        self.threshold = 0.85
    
    def _collect_baseline_data(self, landmarks: LandmarkPoints):
        mid_shoulder = (landmarks.left_shoulder + landmarks.right_shoulder) / 2
        distance = GeometryUtils.calculate_distance(landmarks.nose, mid_shoulder)
        self.calibration_distances.append(distance)
    
    def _finalize_calibration(self):
        if self.calibration_distances:
            self.baseline_distance = np.median(self.calibration_distances)
    
    def _detect_exercise(self, landmarks: LandmarkPoints) -> Tuple[bool, float, dict]:
        mid_shoulder = (landmarks.left_shoulder + landmarks.right_shoulder) / 2
        current_distance = GeometryUtils.calculate_distance(landmarks.nose, mid_shoulder)
        distance_ratio = GeometryUtils.calculate_ratio(current_distance, self.baseline_distance)
        
        detected = distance_ratio < self.threshold
        confidence = max(0.0, min(1.0, (self.threshold - distance_ratio) / 0.15)) if detected else 0.0
        
        metrics = {'distance_ratio': distance_ratio, 'threshold': self.threshold}
        return detected, confidence, metrics
    
    def _generate_status_message(self, detected: bool, confidence: float, metrics: dict) -> str:
        ratio = metrics['distance_ratio']
        if detected:
            return f"💪 FLEXION DETECTED! Keep lowering chin (ratio: {ratio:.2f})"
        return f"🔄 Lower your chin more towards chest (ratio: {ratio:.2f})"


class CervicalExtensionDetector(BaseDetector):
    """Cervical extension detector"""
    
    def __init__(self, config: SystemConfig = None):
        super().__init__(ExerciseType.CERVICAL_EXTENSION, config)
        self.baseline_distance = None
        self.calibration_distances = []
        self.threshold = 1.15
    
    def _collect_baseline_data(self, landmarks: LandmarkPoints):
        mid_shoulder = (landmarks.left_shoulder + landmarks.right_shoulder) / 2
        distance = GeometryUtils.calculate_distance(landmarks.nose, mid_shoulder)
        self.calibration_distances.append(distance)
    
    def _finalize_calibration(self):
        if self.calibration_distances:
            self.baseline_distance = np.median(self.calibration_distances)
    
    def _detect_exercise(self, landmarks: LandmarkPoints) -> Tuple[bool, float, dict]:
        mid_shoulder = (landmarks.left_shoulder + landmarks.right_shoulder) / 2
        current_distance = GeometryUtils.calculate_distance(landmarks.nose, mid_shoulder)
        distance_ratio = GeometryUtils.calculate_ratio(current_distance, self.baseline_distance)
        
        detected = distance_ratio > self.threshold
        confidence = max(0.0, min(1.0, (distance_ratio - self.threshold) / 0.15)) if detected else 0.0
        
        metrics = {'distance_ratio': distance_ratio, 'threshold': self.threshold}
        return detected, confidence, metrics
    
    def _generate_status_message(self, detected: bool, confidence: float, metrics: dict) -> str:
        ratio = metrics['distance_ratio']
        if detected:
            return f"💪 EXTENSION DETECTED! Keep tilting head back (ratio: {ratio:.2f})"
        return f"🔄 Tilt head back more to look upward (ratio: {ratio:.2f})"


class LateralNeckTiltDetector(BaseDetector):
    """Lateral neck tilt detector"""
    
    def __init__(self, config: SystemConfig = None):
        super().__init__(ExerciseType.LATERAL_NECK_TILT, config)
        self.baseline_left = None
        self.baseline_right = None
        self.calibration_left = []
        self.calibration_right = []
        self.threshold = 0.15
    
    def _collect_baseline_data(self, landmarks: LandmarkPoints):
        left_dist = GeometryUtils.calculate_distance(landmarks.nose, landmarks.left_ear)
        right_dist = GeometryUtils.calculate_distance(landmarks.nose, landmarks.right_ear)
        self.calibration_left.append(left_dist)
        self.calibration_right.append(right_dist)
    
    def _finalize_calibration(self):
        if self.calibration_left and self.calibration_right:
            self.baseline_left = np.median(self.calibration_left)
            self.baseline_right = np.median(self.calibration_right)
    
    def _detect_exercise(self, landmarks: LandmarkPoints) -> Tuple[bool, float, dict]:
        left_dist = GeometryUtils.calculate_distance(landmarks.nose, landmarks.left_ear)
        right_dist = GeometryUtils.calculate_distance(landmarks.nose, landmarks.right_ear)
        
        left_ratio = GeometryUtils.calculate_ratio(left_dist, self.baseline_left)
        right_ratio = GeometryUtils.calculate_ratio(right_dist, self.baseline_right)
        ratio_diff = abs(left_ratio - right_ratio)
        
        detected = ratio_diff > self.threshold
        confidence = max(0.0, min(1.0, ratio_diff / 0.3)) if detected else 0.0
        
        direction = "LEFT" if left_ratio < right_ratio else "RIGHT"
        metrics = {'ratio_diff': ratio_diff, 'direction': direction, 'threshold': self.threshold}
        return detected, confidence, metrics
    
    def _generate_status_message(self, detected: bool, confidence: float, metrics: dict) -> str:
        diff = metrics['ratio_diff']
        direction = metrics['direction']
        if detected:
            return f"💪 {direction} TILT DETECTED! (difference: {diff:.2f})"
        return f"🔄 Tilt head more to the side (difference: {diff:.2f})"


class NeckRotationDetector(BaseDetector):
    """Neck rotation detector"""
    
    def __init__(self, config: SystemConfig = None):
        super().__init__(ExerciseType.NECK_ROTATION, config)
        self.baseline_left = None
        self.baseline_right = None
        self.calibration_left = []
        self.calibration_right = []
        self.threshold = 1.5
    
    def _collect_baseline_data(self, landmarks: LandmarkPoints):
        left_vis = abs(landmarks.nose[0] - landmarks.left_ear[0])
        right_vis = abs(landmarks.nose[0] - landmarks.right_ear[0])
        self.calibration_left.append(left_vis)
        self.calibration_right.append(right_vis)
    
    def _finalize_calibration(self):
        if self.calibration_left and self.calibration_right:
            self.baseline_left = np.median(self.calibration_left)
            self.baseline_right = np.median(self.calibration_right)
    
    def _detect_exercise(self, landmarks: LandmarkPoints) -> Tuple[bool, float, dict]:
        left_vis = abs(landmarks.nose[0] - landmarks.left_ear[0])
        right_vis = abs(landmarks.nose[0] - landmarks.right_ear[0])
        
        left_ratio = GeometryUtils.calculate_ratio(left_vis, self.baseline_left)
        right_ratio = GeometryUtils.calculate_ratio(right_vis, self.baseline_right)
        max_ratio = max(left_ratio, right_ratio)
        
        detected = max_ratio > self.threshold
        confidence = max(0.0, min(1.0, (max_ratio - self.threshold) / 1.0)) if detected else 0.0
        
        direction = "RIGHT" if left_ratio > right_ratio else "LEFT"
        metrics = {'max_ratio': max_ratio, 'direction': direction, 'threshold': self.threshold}
        return detected, confidence, metrics
    
    def _generate_status_message(self, detected: bool, confidence: float, metrics: dict) -> str:
        ratio = metrics['max_ratio']
        direction = metrics['direction']
        if detected:
            return f"💪 {direction} ROTATION DETECTED! (ratio: {ratio:.2f})"
        return f"🔄 Turn head more to the side (ratio: {ratio:.2f})"


class ChinTuckDetector(BaseDetector):
    """Chin tuck detector"""
    
    def __init__(self, config: SystemConfig = None):
        super().__init__(ExerciseType.CHIN_TUCK, config)
        self.baseline_offset = None
        self.baseline_depth = None
        self.calibration_offsets = []
        self.calibration_depths = []
        self.threshold = 0.8
    
    def _collect_baseline_data(self, landmarks: LandmarkPoints):
        mid_ear = (landmarks.left_ear + landmarks.right_ear) / 2
        horizontal_offset = abs(landmarks.nose[0] - mid_ear[0])
        vertical_depth = abs(landmarks.nose[1] - mid_ear[1])
        self.calibration_offsets.append(horizontal_offset)
        self.calibration_depths.append(vertical_depth)
    
    def _finalize_calibration(self):
        if self.calibration_offsets and self.calibration_depths:
            self.baseline_offset = np.median(self.calibration_offsets)
            self.baseline_depth = np.median(self.calibration_depths)
    
    def _detect_exercise(self, landmarks: LandmarkPoints) -> Tuple[bool, float, dict]:
        mid_ear = (landmarks.left_ear + landmarks.right_ear) / 2
        horizontal_offset = abs(landmarks.nose[0] - mid_ear[0])
        vertical_depth = abs(landmarks.nose[1] - mid_ear[1])
        
        offset_ratio = GeometryUtils.calculate_ratio(horizontal_offset, self.baseline_offset)
        depth_ratio = GeometryUtils.calculate_ratio(vertical_depth, self.baseline_depth)
        
        detected = offset_ratio < self.threshold and depth_ratio > 1.05
        confidence = max(0.0, min(1.0, (self.threshold - offset_ratio) + (depth_ratio - 1.05))) if detected else 0.0
        
        metrics = {'offset_ratio': offset_ratio, 'depth_ratio': depth_ratio, 'threshold': self.threshold}
        return detected, confidence, metrics
    
    def _generate_status_message(self, detected: bool, confidence: float, metrics: dict) -> str:
        offset = metrics['offset_ratio']
        depth = metrics['depth_ratio']
        if detected:
            return f"💪 CHIN TUCK DETECTED! (offset: {offset:.2f}, depth: {depth:.2f})"
        return f"🔄 Pull chin back more (offset: {offset:.2f})"


class ExerciseDetectionSystem:
    """Main system that coordinates all exercise detectors"""
    
    def __init__(self, config: SystemConfig = None):
        self.config = config or SystemConfig()
        self.landmark_extractor = LandmarkExtractor()
        
        # Initialize all detectors
        self.detectors = {
            ExerciseType.CERVICAL_FLEXION: CervicalFlexionDetector(self.config),
            ExerciseType.CERVICAL_EXTENSION: CervicalExtensionDetector(self.config),
            ExerciseType.LATERAL_NECK_TILT: LateralNeckTiltDetector(self.config),
            ExerciseType.NECK_ROTATION: NeckRotationDetector(self.config),
            ExerciseType.CHIN_TUCK: ChinTuckDetector(self.config)
        }
        
        # System state
        self.total_detections = 0
        self.session_start_time = time.time()
    
    def detect_exercises(self, pose_results, frame_shape) -> Dict[ExerciseType, ExerciseResult]:
        """Detect all exercises from pose results"""
        # Extract landmarks
        landmarks = self.landmark_extractor.extract_landmarks(pose_results, frame_shape)
        
        results = {}
        self.total_detections += 1
        
        # Run detection for each exercise
        for exercise_type, detector in self.detectors.items():
            try:
                result = detector.detect(landmarks)
                results[exercise_type] = result
            except Exception as e:
                # Fallback error result
                results[exercise_type] = ExerciseResult(
                    exercise_type, False, 0.0, DetectionStatus.ERROR,
                    f"Error: {str(e)}"
                )
        
        return results
    
    def reset_baselines(self):
        """Reset all detector baselines"""
        for detector in self.detectors.values():
            detector.reset()
    
    def get_system_stats(self) -> dict:
        """Get detection system statistics"""
        session_duration = time.time() - self.session_start_time
        
        return {
            'total_detections': self.total_detections,
            'session_duration': session_duration,
            'detections_per_second': self.total_detections / session_duration if session_duration > 0 else 0,
            'active_detectors': len(self.detectors)
        }
        return self.detectors.get(exercise_type)
    
    def reset_baselines(self):
        """Reset all detector baselines"""
        for detector in self.detectors.values():
            detector.reset()
        
        self.total_detections = 0
        self.session_start_time = time.time()
    
    def get_system_stats(self) -> dict:
        """Get system performance statistics"""
        session_duration = time.time() - self.session_start_time
        
        # Count calibrated detectors
        calibrated_count = sum(
            1 for detector in self.detectors.values() 
            if detector.calibration.is_complete
        )
        
        return {
            'total_detections': self.total_detections,
            'session_duration': session_duration,
            'detections_per_second': self.total_detections / max(session_duration, 1),
            'calibrated_detectors': calibrated_count,
            'total_detectors': len(self.detectors)
        }
    
    def is_fully_calibrated(self) -> bool:
        """Check if all detectors are calibrated"""
        return all(
            detector.calibration.is_complete 
            for detector in self.detectors.values()
        )
    
    def get_calibration_progress(self) -> dict:
        """Get calibration progress for all detectors"""
        progress = {}
        for exercise_type, detector in self.detectors.items():
            progress[exercise_type] = {
                'progress_percentage': detector.calibration.progress_percentage,
                'frames_collected': detector.calibration.frames_collected,
                'frames_required': detector.calibration.frames_required,
                'is_complete': detector.calibration.is_complete
            }
        return progress
