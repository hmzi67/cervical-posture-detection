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
            
            # Try multiple initialization methods
            initialization_methods = []
            
            if platform.system() == "Darwin":  # macOS
                initialization_methods = [
                    (camera_index, cv2.CAP_AVFOUNDATION if hasattr(cv2, 'CAP_AVFOUNDATION') else cv2.CAP_ANY),
                    (camera_index, cv2.CAP_ANY),
                    (0, cv2.CAP_AVFOUNDATION if hasattr(cv2, 'CAP_AVFOUNDATION') else cv2.CAP_ANY),
                    (0, cv2.CAP_ANY)
                ]
            else:
                initialization_methods = [
                    (camera_index, backend),
                    (camera_index, cv2.CAP_ANY),
                    (0, cv2.CAP_ANY)
                ]
            
            # Remove duplicates while preserving order
            seen = set()
            unique_methods = []
            for method in initialization_methods:
                if method not in seen:
                    unique_methods.append(method)
                    seen.add(method)
            
            # Try each initialization method
            for idx, backend_to_try in unique_methods:
                print(f"Trying camera {idx} with backend {backend_to_try}")
                
                try:
                    self.cap = cv2.VideoCapture(idx, backend_to_try)
                    
                    if not self.cap.isOpened():
                        print(f"Failed to open camera {idx} - camera.isOpened() returned False")
                        if self.cap:
                            self.cap.release()
                        continue
                    
                    print(f"Camera {idx} opened successfully with backend {backend_to_try}")
                    
                    # Test if this camera actually works
                    if self._test_camera_capture():
                        self.camera_index = idx
                        return True
                    else:
                        print(f"Camera {idx} opened but failed frame capture test")
                        self.cap.release()
                        continue
                        
                except Exception as init_error:
                    print(f"Error initializing camera {idx} with backend {backend_to_try}: {init_error}")
                    if self.cap:
                        self.cap.release()
                    continue
            
            print("All camera initialization methods failed")
            return False
            
        except Exception as e:
            print(f"Camera initialization exception: {e}")
            import traceback
            traceback.print_exc()
            st.error(f"Camera initialization error: {e}")
            if self.cap:
                self.cap.release()
            return False
    
    def _test_camera_capture(self) -> bool:
        """Test if camera can actually capture frames"""
        if not self.cap or not self.cap.isOpened():
            return False
        
        # Give camera more time to initialize (especially important on macOS)
        print("Allowing camera to initialize...")
        time.sleep(1.5)  # Increased from 1.0 to 1.5 seconds
        
        # Set camera properties with error checking
        try:
            # Set buffer size first to reduce latency
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            # Set frame dimensions
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            # Set FPS - but be flexible if it fails
            try:
                self.cap.set(cv2.CAP_PROP_FPS, 30)
            except:
                print("Warning: Could not set FPS, using default")
            
            # Additional macOS-specific settings
            if platform.system() == "Darwin":
                try:
                    # Try to set format to MJPG for better compatibility
                    self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
                except:
                    print("Warning: Could not set MJPG format")
                    # Try alternative format
                    try:
                        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'YUYV'))
                    except:
                        print("Warning: Could not set YUYV format either")
            
            print("Camera properties set successfully")
        except Exception as prop_error:
            print(f"Warning: Failed to set camera properties: {prop_error}")
        
        # Clear any buffered frames first
        print("Clearing camera buffer...")
        for _ in range(20):  # Increased buffer clearing
            try:
                ret, frame = self.cap.read()
                if ret and frame is not None:
                    # Successfully read a frame during buffer clearing
                    print("Got frame during buffer clearing - camera is working!")
            except:
                break
        
        # Give additional time after clearing buffer
        time.sleep(1.0)  # Increased delay
        
        # Test frame capture multiple times with longer delays
        for attempt in range(15):  # More attempts
            print(f"Attempting to read frame (attempt {attempt + 1}/15)")
            try:
                ret, frame = self.cap.read()
                if ret and frame is not None and frame.size > 0:
                    print(f"Successfully captured frame: {frame.shape}")
                    self.is_running = True
                    self.error_count = 0
                    return True
                else:
                    frame_info = 'None' if frame is None else f'shape={frame.shape}' if hasattr(frame, 'shape') else 'invalid'
                    print(f"Frame capture failed on attempt {attempt + 1}: ret={ret}, frame={frame_info}")
            except Exception as read_error:
                print(f"Exception during frame read attempt {attempt + 1}: {read_error}")
            
            # Progressive delay - longer waits for later attempts
            delay = 0.5 + (attempt * 0.2)  # Increased delays
            time.sleep(delay)
        
        print(f"Camera opened but failed to capture frames after 15 attempts")
        return False
    
    def read_frame(self) -> Optional[np.ndarray]:
        """Read frame with error recovery"""
        if not self.cap or not self.is_running:
            return None
        
        try:
            ret, frame = self.cap.read()
            if ret and frame is not None:
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
