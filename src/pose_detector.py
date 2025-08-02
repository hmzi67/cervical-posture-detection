"""
Enhanced pose detection with cervical-specific analysis
"""
import cv2
import mediapipe as mp
import numpy as np
from typing import Dict, Optional, Tuple

class CervicalPoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Define cervical-specific landmarks
        self.cervical_landmarks = [
            self.mp_pose.PoseLandmark.NOSE,
            self.mp_pose.PoseLandmark.LEFT_EAR,
            self.mp_pose.PoseLandmark.RIGHT_EAR,
            self.mp_pose.PoseLandmark.MOUTH_LEFT,
            self.mp_pose.PoseLandmark.MOUTH_RIGHT,
            self.mp_pose.PoseLandmark.LEFT_SHOULDER,
            self.mp_pose.PoseLandmark.RIGHT_SHOULDER,
        ]
    
    def detect_pose(self, frame: np.ndarray) -> Tuple[Optional[Dict], np.ndarray]:
        """
        Detect pose with focus on cervical region
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        
        annotated_frame = frame.copy()
        cervical_landmarks = None
        
        if results.pose_landmarks:
            # Draw all landmarks
            self.mp_drawing.draw_landmarks(
                annotated_frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
            
            # Extract cervical-specific landmarks
            cervical_landmarks = self._extract_cervical_landmarks(results.pose_landmarks)
            
            # Highlight cervical region
            self._highlight_cervical_region(annotated_frame, cervical_landmarks)
        
        return cervical_landmarks, annotated_frame
    
    def _extract_cervical_landmarks(self, pose_landmarks) -> Dict:
        """Extract key landmarks for cervical analysis"""
        landmarks = pose_landmarks.landmark
        
        return {
            'nose': landmarks[self.mp_pose.PoseLandmark.NOSE],
            'left_ear': landmarks[self.mp_pose.PoseLandmark.LEFT_EAR],
            'right_ear': landmarks[self.mp_pose.PoseLandmark.RIGHT_EAR],
            'left_shoulder': landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER],
            'right_shoulder': landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER],
            'left_mouth': landmarks[self.mp_pose.PoseLandmark.MOUTH_LEFT],
            'right_mouth': landmarks[self.mp_pose.PoseLandmark.MOUTH_RIGHT],
        }
    
    def _highlight_cervical_region(self, frame: np.ndarray, landmarks: Dict):
        """Draw additional highlights for cervical region"""
        if not landmarks:
            return
        
        h, w = frame.shape[:2]
        
        # Convert normalized coordinates to pixel coordinates
        nose_px = (int(landmarks['nose'].x * w), int(landmarks['nose'].y * h))
        left_ear_px = (int(landmarks['left_ear'].x * w), int(landmarks['left_ear'].y * h))
        right_ear_px = (int(landmarks['right_ear'].x * w), int(landmarks['right_ear'].y * h))
        left_shoulder_px = (int(landmarks['left_shoulder'].x * w), int(landmarks['left_shoulder'].y * h))
        right_shoulder_px = (int(landmarks['right_shoulder'].x * w), int(landmarks['right_shoulder'].y * h))
        
        # Draw cervical region outline
        cv2.circle(frame, nose_px, 8, (0, 255, 0), -1)  # Green nose
        cv2.circle(frame, left_ear_px, 6, (255, 0, 0), -1)  # Blue ears
        cv2.circle(frame, right_ear_px, 6, (255, 0, 0), -1)
        
        # Draw reference lines
        cv2.line(frame, left_shoulder_px, right_shoulder_px, (255, 255, 0), 2)  # Shoulder line
        cv2.line(frame, left_ear_px, right_ear_px, (0, 255, 255), 2)  # Head line