"""
Video processing and pose detection for the cervical pose detection system.
"""
import cv2
import mediapipe as mp
import numpy as np
import time
from typing import Dict, Tuple

from .models import ExerciseType, ExerciseResult, DetectionStatus, SystemConfig
from .detection_system import ExerciseDetectionSystem


class VideoProcessor:
    """Video processing and pose detection"""
    
    def __init__(self, config: SystemConfig = None):
        self.config = config or SystemConfig()
        
        # Initialize MediaPipe
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Initialize exercise detection system
        self.exercise_system = ExerciseDetectionSystem()
        
        # Performance tracking
        self.processing_times = []
        self.frame_count = 0
    
    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Dict[ExerciseType, ExerciseResult]]:
        """Process a single frame and return results"""
        start_time = time.time()
        
        # Validate input frame
        if frame is None:
            # Return a blank frame and error results
            blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            error_results = {
                exercise_type: ExerciseResult(
                    exercise_type, False, 0.0, DetectionStatus.ERROR,
                    "No frame provided"
                ) for exercise_type in ExerciseType
            }
            return blank_frame, error_results
        
        try:
            # Convert BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe
            pose_results = self.pose.process(rgb_frame)
            
            # Draw pose landmarks
            if pose_results.pose_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, pose_results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=4, circle_radius=4),
                    connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=3)
                )
            
            # Detect exercises
            exercise_results = self.exercise_system.detect_exercises(pose_results, frame.shape)
            
            # Draw FPS
            self._draw_fps(frame)
            
            # Update performance metrics
            processing_time = time.time() - start_time
            self.processing_times.append(processing_time)
            if len(self.processing_times) > 30:
                self.processing_times.pop(0)
            
            self.frame_count += 1
            
            return frame, exercise_results
            
        except Exception as e:
            # Handle any processing errors gracefully
            error_results = {
                exercise_type: ExerciseResult(
                    exercise_type, False, 0.0, DetectionStatus.ERROR,
                    f"Processing error: {str(e)}"
                ) for exercise_type in ExerciseType
            }
            return frame.copy() if frame is not None else np.zeros((480, 640, 3), dtype=np.uint8), error_results
    
    def _draw_fps(self, frame: np.ndarray):
        """Draw FPS on frame"""
        if self.processing_times:
            fps = 1.0 / np.mean(self.processing_times)
            h, w = frame.shape[:2]
            cv2.putText(frame, f"FPS: {fps:.1f}", (w - 110, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def reset_baselines(self):
        """Reset all detector baselines"""
        self.exercise_system.reset_baselines()
    
    def get_system_stats(self) -> dict:
        """Get system performance statistics"""
        avg_fps = 0
        if self.processing_times:
            avg_fps = 1.0 / np.mean(self.processing_times)
        
        return {
            'frame_count': self.frame_count,
            'avg_fps': avg_fps,
            'avg_processing_time': np.mean(self.processing_times) if self.processing_times else 0,
            'detectors_count': len(self.exercise_system.detectors)
        }
    
    def cleanup(self):
        """Cleanup MediaPipe resources"""
        if hasattr(self, 'pose'):
            self.pose.close()