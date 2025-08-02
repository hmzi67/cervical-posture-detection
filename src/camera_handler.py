"""
Enhanced camera handler with comprehensive error handling
"""
import cv2
import streamlit as st
import numpy as np
import platform
import time
from typing import Optional, Tuple

class FixedCameraHandler:
    def __init__(self):
        self.cap = None
        self.is_running = False
        self.camera_index = 0
        self.last_frame = None
        self.error_count = 0
        self.max_errors = 5
    
    def find_available_cameras(self) -> list:
        """Find all available camera indices"""
        available_cameras = []
        
        print("Searching for available cameras...")
        
        # Check different camera backends
        backends = [cv2.CAP_ANY]
        
        try:
            if platform.system() == "Darwin":  # macOS
                if hasattr(cv2, 'CAP_AVFOUNDATION'):
                    backends.append(cv2.CAP_AVFOUNDATION)
                # CAP_QTKIT is deprecated in newer OpenCV versions
                if hasattr(cv2, 'CAP_QTKIT'):
                    backends.append(cv2.CAP_QTKIT)
            elif platform.system() == "Windows":
                if hasattr(cv2, 'CAP_DSHOW'):
                    backends.append(cv2.CAP_DSHOW)
                if hasattr(cv2, 'CAP_MSMF'):
                    backends.append(cv2.CAP_MSMF)
            elif platform.system() == "Linux":
                if hasattr(cv2, 'CAP_V4L2'):
                    backends.append(cv2.CAP_V4L2)
        except AttributeError as e:
            print(f"Some camera backends not available: {e}")
            # Fallback to just CAP_ANY
        
        for backend in backends:
            print(f"Testing backend: {backend}")
            for i in range(5):
                try:
                    cap = cv2.VideoCapture(i, backend)
                    if cap.isOpened():
                        # Try to read a frame to verify the camera actually works
                        ret, frame = cap.read()
                        if ret and frame is not None:
                            print(f"Found working camera at index {i} with backend {backend}")
                            available_cameras.append((i, backend))
                        cap.release()
                        time.sleep(0.1)  # Small delay between attempts
                except Exception as e:
                    print(f"Error testing camera {i} with backend {backend}: {e}")
                    pass
        
        print(f"Total cameras found: {len(available_cameras)}")
        return available_cameras
    
    def start_camera(self, camera_index: int = 0, backend: int = cv2.CAP_ANY) -> bool:
        """Initialize camera with enhanced error handling"""
        try:
            # Release any existing camera
            if self.cap:
                self.cap.release()
                time.sleep(0.5)  # Give time for camera to release
            
            print(f"Attempting to open camera {camera_index} with backend {backend}")
            
            # Try to open camera with specified backend
            self.cap = cv2.VideoCapture(camera_index, backend)
            
            if not self.cap.isOpened():
                print(f"Failed to open camera {camera_index} - camera.isOpened() returned False")
                # Try alternative method for macOS
                if platform.system() == "Darwin":
                    print("Trying alternative camera initialization for macOS...")
                    self.cap = cv2.VideoCapture(camera_index)
                    if not self.cap.isOpened():
                        print("Alternative method also failed")
                        return False
                else:
                    return False
            
            print(f"Camera {camera_index} opened successfully")
            
            # Set camera properties with error checking
            try:
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.cap.set(cv2.CAP_PROP_FPS, 30)
                print("Camera properties set successfully")
            except Exception as prop_error:
                print(f"Warning: Failed to set camera properties: {prop_error}")
            
            # Test frame capture multiple times
            for attempt in range(5):
                print(f"Attempting to read frame (attempt {attempt + 1}/5)")
                ret, frame = self.cap.read()
                if ret and frame is not None:
                    print(f"Successfully captured frame: {frame.shape}")
                    self.is_running = True
                    self.camera_index = camera_index
                    self.error_count = 0
                    return True
                else:
                    print(f"Frame capture failed on attempt {attempt + 1}: ret={ret}, frame={'None' if frame is None else 'exists'}")
                time.sleep(0.2)
            
            print(f"Camera {camera_index} opened but failed to capture frames after 5 attempts")
            self.cap.release()
            return False
            
        except Exception as e:
            print(f"Camera initialization exception: {e}")
            import traceback
            traceback.print_exc()
            st.error(f"Camera initialization error: {e}")
            if self.cap:
                self.cap.release()
            return False
    
    def read_frame(self) -> Optional[np.ndarray]:
        """Read frame with error recovery"""
        if not self.cap or not self.is_running:
            return None
        
        try:
            ret, frame = self.cap.read()
            if ret:
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                self.last_frame = frame
                self.error_count = 0
                return frame
            else:
                self.error_count += 1
                if self.error_count >= self.max_errors:
                    st.error("Too many camera errors. Restarting camera...")
                    self.restart_camera()
                return self.last_frame  # Return last good frame
                
        except Exception as e:
            st.error(f"Frame read error: {e}")
            self.error_count += 1
            return self.last_frame
    
    def restart_camera(self):
        """Restart camera connection"""
        if self.cap:
            self.cap.release()
        time.sleep(1)
        self.start_camera(self.camera_index)
    
    def stop_camera(self):
        """Stop camera and release resources"""
        self.is_running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        cv2.destroyAllWindows()
    
    def get_camera_info(self) -> dict:
        """Get current camera information"""
        if not self.cap:
            return {}
        
        return {
            'width': int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fps': self.cap.get(cv2.CAP_PROP_FPS),
            'backend': self.cap.get(cv2.CAP_PROP_BACKEND),
            'index': self.camera_index
        }