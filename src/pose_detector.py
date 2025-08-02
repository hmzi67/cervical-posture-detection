"""
Pose detection using MediaPipe
"""
import cv2
import mediapipe as mp
import numpy as np

class PoseDetector:
    def __init__(self, 
                 static_image_mode=False,
                 model_complexity=1,
                 enable_segmentation=False,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.pose = self.mp_pose.Pose(
            static_image_mode=static_image_mode,
            model_complexity=model_complexity,
            enable_segmentation=enable_segmentation,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
    
    def detect_pose(self, frame):
        """
        Detect pose landmarks in a frame
        
        Args:
            frame: Input image/frame
            
        Returns:
            results: MediaPipe pose detection results
            annotated_frame: Frame with pose landmarks drawn
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.pose.process(rgb_frame)
        
        # Draw landmarks on the frame
        annotated_frame = frame.copy()
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                annotated_frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
        
        return results, annotated_frame
    
    def get_key_landmarks(self, results):
        """
        Extract key landmarks for cervical exercises
        
        Args:
            results: MediaPipe pose detection results
            
        Returns:
            landmarks_dict: Dictionary with key landmark coordinates
        """
        if not results.pose_landmarks:
            return None
        
        landmarks = results.pose_landmarks.landmark
        
        # Key landmarks for cervical exercises
        key_landmarks = {
            'nose': landmarks[self.mp_pose.PoseLandmark.NOSE],
            'left_ear': landmarks[self.mp_pose.PoseLandmark.LEFT_EAR],
            'right_ear': landmarks[self.mp_pose.PoseLandmark.RIGHT_EAR],
            'left_shoulder': landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER],
            'right_shoulder': landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER],
            'left_mouth': landmarks[self.mp_pose.PoseLandmark.MOUTH_LEFT],
            'right_mouth': landmarks[self.mp_pose.PoseLandmark.MOUTH_RIGHT],
        }
        
        return key_landmarks