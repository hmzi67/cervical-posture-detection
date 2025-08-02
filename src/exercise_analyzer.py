"""
Exercise-specific analysis for cervical movements
"""
import numpy as np
from typing import Dict, List, Tuple, Optional
from src.utils import calculate_angle, calculate_distance

class CervicalExerciseAnalyzer:
    def __init__(self):
        self.exercise_thresholds = {
            'cervical_flexion': {'min_angle': 30, 'max_angle': 60},
            'cervical_extension': {'min_angle': 15, 'max_angle': 45},
            'lateral_tilt': {'min_angle': 20, 'max_angle': 45},
            'rotation': {'min_angle': 30, 'max_angle': 80},
            'chin_tuck': {'min_distance': 0.02, 'max_distance': 0.08}
        }
    
    def analyze_cervical_flexion(self, landmarks: Dict) -> Dict:
        """Analyze chin-to-chest movement"""
        if not landmarks:
            return {'angle': 0, 'status': 'No pose detected', 'feedback': ''}
        
        # Calculate angle between nose-shoulder line and vertical
        nose = [landmarks['nose'].x, landmarks['nose'].y]
        left_shoulder = [landmarks['left_shoulder'].x, landmarks['left_shoulder'].y]
        right_shoulder = [landmarks['right_shoulder'].x, landmarks['right_shoulder'].y]
        
        # Midpoint of shoulders
        shoulder_midpoint = [
            (left_shoulder[0] + right_shoulder[0]) / 2,
            (left_shoulder[1] + right_shoulder[1]) / 2
        ]
        
        # Calculate head forward angle
        vertical_point = [shoulder_midpoint[0], shoulder_midpoint[1] - 0.1]
        angle = calculate_angle(vertical_point, shoulder_midpoint, nose)
        
        # Determine status
        thresholds = self.exercise_thresholds['cervical_flexion']
        if angle >= thresholds['min_angle'] and angle <= thresholds['max_angle']:
            status = 'Good'
            feedback = 'Perfect flexion angle!'
        elif angle < thresholds['min_angle']:
            status = 'Too little'
            feedback = 'Tuck your chin closer to chest'
        else:
            status = 'Too much'
            feedback = 'Don\'t strain - less flexion needed'
        
        return {
            'angle': round(angle, 1),
            'status': status,
            'feedback': feedback,
            'exercise': 'Cervical Flexion'
        }
    
    def analyze_cervical_extension(self, landmarks: Dict) -> Dict:
        """Analyze looking upward movement"""
        if not landmarks:
            return {'angle': 0, 'status': 'No pose detected', 'feedback': ''}
        
        nose = [landmarks['nose'].x, landmarks['nose'].y]
        left_shoulder = [landmarks['left_shoulder'].x, landmarks['left_shoulder'].y]
        right_shoulder = [landmarks['right_shoulder'].x, landmarks['right_shoulder'].y]
        
        shoulder_midpoint = [
            (left_shoulder[0] + right_shoulder[0]) / 2,
            (left_shoulder[1] + right_shoulder[1]) / 2
        ]
        
        # Check if head is tilted back (nose higher than normal)
        head_tilt = shoulder_midpoint[1] - nose[1]
        angle = abs(head_tilt * 100)  # Convert to approximate angle
        
        thresholds = self.exercise_thresholds['cervical_extension']
        if angle >= thresholds['min_angle'] and angle <= thresholds['max_angle']:
            status = 'Good'
            feedback = 'Good extension - hold position!'
        elif angle < thresholds['min_angle']:
            status = 'Too little'
            feedback = 'Tilt head back more gently'
        else:
            status = 'Too much'
            feedback = 'Don\'t hyperextend - ease back'
        
        return {
            'angle': round(angle, 1),
            'status': status,
            'feedback': feedback,
            'exercise': 'Cervical Extension'
        }
    
    def analyze_lateral_tilt(self, landmarks: Dict) -> Dict:
        """Analyze left/right head tilt"""
        if not landmarks:
            return {'angle': 0, 'status': 'No pose detected', 'feedback': ''}
        
        left_ear = [landmarks['left_ear'].x, landmarks['left_ear'].y]
        right_ear = [landmarks['right_ear'].x, landmarks['right_ear'].y]
        left_shoulder = [landmarks['left_shoulder'].x, landmarks['left_shoulder'].y]
        right_shoulder = [landmarks['right_shoulder'].x, landmarks['right_shoulder'].y]
        
        # Calculate head tilt angle
        ear_midpoint = [(left_ear[0] + right_ear[0]) / 2, (left_ear[1] + right_ear[1]) / 2]
        shoulder_line = [right_shoulder[0] - left_shoulder[0], right_shoulder[1] - left_shoulder[1]]
        ear_line = [right_ear[0] - left_ear[0], right_ear[1] - left_ear[1]]
        
        # Calculate angle between shoulder line and ear line
        dot_product = shoulder_line[0] * ear_line[0] + shoulder_line[1] * ear_line[1]
        magnitude_shoulder = np.sqrt(shoulder_line[0]**2 + shoulder_line[1]**2)
        magnitude_ear = np.sqrt(ear_line[0]**2 + ear_line[1]**2)
        
        if magnitude_shoulder > 0 and magnitude_ear > 0:
            cos_angle = dot_product / (magnitude_shoulder * magnitude_ear)
            angle = np.arccos(np.clip(cos_angle, -1, 1)) * 180 / np.pi
        else:
            angle = 0
        
        thresholds = self.exercise_thresholds['lateral_tilt']
        if angle >= thresholds['min_angle'] and angle <= thresholds['max_angle']:
            status = 'Good'
            feedback = 'Perfect lateral tilt!'
        elif angle < thresholds['min_angle']:
            status = 'Too little'
            feedback = 'Tilt head more to the side'
        else:
            status = 'Too much'
            feedback = 'Don\'t force - gentle tilt only'
        
        return {
            'angle': round(angle, 1),
            'status': status,
            'feedback': feedback,
            'exercise': 'Lateral Neck Tilt'
        }
    
    def analyze_neck_rotation(self, landmarks: Dict) -> Dict:
        """Analyze left/right head rotation"""
        if not landmarks:
            return {'angle': 0, 'status': 'No pose detected', 'feedback': ''}
        
        nose = [landmarks['nose'].x, landmarks['nose'].y]
        left_ear = [landmarks['left_ear'].x, landmarks['left_ear'].y]
        right_ear = [landmarks['right_ear'].x, landmarks['right_ear'].y]
        
        # Calculate face orientation
        ear_distance_diff = abs(
            calculate_distance(nose, left_ear) - calculate_distance(nose, right_ear)
        )
        
        # Convert to approximate rotation angle
        angle = ear_distance_diff * 1000  # Scale for visibility
        
        thresholds = self.exercise_thresholds['rotation']
        if angle >= thresholds['min_angle'] and angle <= thresholds['max_angle']:
            status = 'Good'
            feedback = 'Good rotation range!'
        elif angle < thresholds['min_angle']:
            status = 'Too little'
            feedback = 'Turn head more to the side'
        else:
            status = 'Too much'
            feedback = 'Don\'t strain - turn back slightly'
        
        return {
            'angle': round(angle, 1),
            'status': status,
            'feedback': feedback,
            'exercise': 'Neck Rotation'
        }
    
    def analyze_chin_tuck(self, landmarks: Dict) -> Dict:
        """Analyze chin retraction movement"""
        if not landmarks:
            return {'distance': 0, 'status': 'No pose detected', 'feedback': ''}
        
        nose = [landmarks['nose'].x, landmarks['nose'].y]
        left_shoulder = [landmarks['left_shoulder'].x, landmarks['left_shoulder'].y]
        right_shoulder = [landmarks['right_shoulder'].x, landmarks['right_shoulder'].y]
        
        # Calculate forward head posture
        shoulder_midpoint = [
            (left_shoulder[0] + right_shoulder[0]) / 2,
            (left_shoulder[1] + right_shoulder[1]) / 2
        ]
        
        forward_distance = nose[0] - shoulder_midpoint[0]
        
        thresholds = self.exercise_thresholds['chin_tuck']
        if forward_distance >= thresholds['min_distance'] and forward_distance <= thresholds['max_distance']:
            status = 'Good'
            feedback = 'Perfect chin tuck position!'
        elif forward_distance > thresholds['max_distance']:
            status = 'Forward head'
            feedback = 'Pull chin back more'
        else:
            status = 'Over-tucked'
            feedback = 'Relax - don\'t over-tuck'
        
        return {
            'distance': round(abs(forward_distance) * 100, 1),
            'status': status,
            'feedback': feedback,
            'exercise': 'Chin Tuck'
        }