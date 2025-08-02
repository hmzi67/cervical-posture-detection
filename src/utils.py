"""
Utility functions for the cervical posture detection app
"""
import numpy as np
import cv2
import mediapipe as mp

def calculate_angle(a, b, c):
    """
    Calculate angle between three points
    
    Args:
        a, b, c: Points as [x, y] coordinates
        b is the vertex of the angle
    
    Returns:
        angle: Angle in degrees
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points"""
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def normalize_landmarks(landmarks, frame_width, frame_height):
    """Convert normalized landmarks to pixel coordinates"""
    normalized = []
    for landmark in landmarks:
        x = int(landmark.x * frame_width)
        y = int(landmark.y * frame_height)
        normalized.append([x, y])
    return normalized