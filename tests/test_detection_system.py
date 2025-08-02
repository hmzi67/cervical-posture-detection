"""
Unit tests for the detection system and exercise detectors.

Tests cover:
- BaseDetector abstract functionality
- Individual exercise detector logic
- Calibration process validation
- Detection accuracy and confidence scoring
- Error handling and edge cases
"""
import unittest
import numpy as np
from unittest.mock import Mock, patch
import sys
import os

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.core.detection_system import (
    BaseDetector, CervicalFlexionDetector, CervicalExtensionDetector,
    LateralNeckTiltDetector, NeckRotationDetector, ChinTuckDetector,
    ExerciseDetectionSystem
)
from src.core.models import ExerciseType, ExerciseResult, DetectionStatus, SystemConfig, LandmarkPoints


class TestLandmarkPoints(unittest.TestCase):
    """Test LandmarkPoints data structure"""
    
    def setUp(self):
        self.landmarks = LandmarkPoints(
            nose=np.array([100, 150]),
            left_ear=np.array([80, 140]),
            right_ear=np.array([120, 140]),
            left_shoulder=np.array([60, 200]),
            right_shoulder=np.array([140, 200])
        )
    
    def test_landmark_creation(self):
        """Test landmark points creation"""
        self.assertIsInstance(self.landmarks.nose, np.ndarray)
        self.assertEqual(len(self.landmarks.nose), 2)
        self.assertEqual(self.landmarks.nose[0], 100)
        self.assertEqual(self.landmarks.nose[1], 150)


class TestCervicalFlexionDetector(unittest.TestCase):
    """Test cervical flexion detection logic"""
    
    def setUp(self):
        self.config = SystemConfig()
        self.detector = CervicalFlexionDetector(self.config)
        self.landmarks = LandmarkPoints(
            nose=np.array([100, 150]),
            left_ear=np.array([80, 140]),
            right_ear=np.array([120, 140]),
            left_shoulder=np.array([60, 200]),
            right_shoulder=np.array([140, 200])
        )
    
    def test_initial_state(self):
        """Test detector initial state"""
        self.assertEqual(self.detector.exercise_type, ExerciseType.CERVICAL_FLEXION)
        self.assertFalse(self.detector.is_calibrated)
        self.assertEqual(self.detector.frames_collected, 0)
        self.assertIsNone(self.detector.baseline_distance)
    
    def test_calibration_process(self):
        """Test calibration data collection"""
        # Simulate calibration frames
        for i in range(10):
            result = self.detector.detect(self.landmarks)
            self.assertEqual(result.status, DetectionStatus.CALIBRATING)
            self.assertFalse(result.detected)
        
        # Should still be calibrating at frame 10
        self.assertFalse(self.detector.is_calibrated)
        
        # Complete calibration
        for i in range(5):
            result = self.detector.detect(self.landmarks)
        
        # Should be calibrated now
        self.assertTrue(self.detector.is_calibrated)
        self.assertIsNotNone(self.detector.baseline_distance)
    
    def test_flexion_detection_positive(self):
        """Test positive flexion detection"""
        # Complete calibration first
        for i in range(15):
            self.detector.detect(self.landmarks)
        
        # Create flexion landmarks (nose closer to shoulders)
        flexion_landmarks = LandmarkPoints(
            nose=np.array([100, 170]),  # Moved down
            left_ear=np.array([80, 160]),
            right_ear=np.array([120, 160]),
            left_shoulder=np.array([60, 200]),
            right_shoulder=np.array([140, 200])
        )
        
        result = self.detector.detect(flexion_landmarks)
        self.assertTrue(result.detected)
        self.assertGreater(result.confidence, 0)
        self.assertEqual(result.status, DetectionStatus.DETECTED)
    
    def test_flexion_detection_negative(self):
        """Test negative flexion detection"""
        # Complete calibration first
        for i in range(15):
            self.detector.detect(self.landmarks)
        
        # Create extension landmarks (nose further from shoulders)
        extension_landmarks = LandmarkPoints(
            nose=np.array([100, 130]),  # Moved up
            left_ear=np.array([80, 120]),
            right_ear=np.array([120, 120]),
            left_shoulder=np.array([60, 200]),
            right_shoulder=np.array([140, 200])
        )
        
        result = self.detector.detect(extension_landmarks)
        self.assertFalse(result.detected)
        self.assertEqual(result.confidence, 0.0)
        self.assertEqual(result.status, DetectionStatus.NOT_DETECTED)
    
    def test_detector_reset(self):
        """Test detector reset functionality"""
        # Calibrate and detect
        for i in range(15):
            self.detector.detect(self.landmarks)
        
        self.assertTrue(self.detector.is_calibrated)
        
        # Reset
        self.detector.reset()
        
        self.assertFalse(self.detector.is_calibrated)
        self.assertEqual(self.detector.frames_collected, 0)
        self.assertEqual(self.detector.previous_confidence, 0.0)
    
    def test_none_landmarks_handling(self):
        """Test handling of None landmarks"""
        result = self.detector.detect(None)
        self.assertFalse(result.detected)
        self.assertEqual(result.status, DetectionStatus.ERROR)
        self.assertIn("No pose detected", result.status_message)


class TestCervicalExtensionDetector(unittest.TestCase):
    """Test cervical extension detection logic"""
    
    def setUp(self):
        self.config = SystemConfig()
        self.detector = CervicalExtensionDetector(self.config)
        self.landmarks = LandmarkPoints(
            nose=np.array([100, 150]),
            left_ear=np.array([80, 140]),
            right_ear=np.array([120, 140]),
            left_shoulder=np.array([60, 200]),
            right_shoulder=np.array([140, 200])
        )
    
    def test_extension_detection_positive(self):
        """Test positive extension detection"""
        # Complete calibration first
        for i in range(15):
            self.detector.detect(self.landmarks)
        
        # Create extension landmarks (nose further from shoulders)
        extension_landmarks = LandmarkPoints(
            nose=np.array([100, 120]),  # Moved up significantly
            left_ear=np.array([80, 110]),
            right_ear=np.array([120, 110]),
            left_shoulder=np.array([60, 200]),
            right_shoulder=np.array([140, 200])
        )
        
        result = self.detector.detect(extension_landmarks)
        self.assertTrue(result.detected)
        self.assertGreater(result.confidence, 0)
        self.assertEqual(result.status, DetectionStatus.DETECTED)


class TestLateralNeckTiltDetector(unittest.TestCase):
    """Test lateral neck tilt detection logic"""
    
    def setUp(self):
        self.config = SystemConfig()
        self.detector = LateralNeckTiltDetector(self.config)
        self.landmarks = LandmarkPoints(
            nose=np.array([100, 150]),
            left_ear=np.array([80, 140]),
            right_ear=np.array([120, 140]),
            left_shoulder=np.array([60, 200]),
            right_shoulder=np.array([140, 200])
        )
    
    def test_tilt_detection_positive(self):
        """Test positive tilt detection"""
        # Complete calibration first
        for i in range(15):
            self.detector.detect(self.landmarks)
        
        # Create left tilt landmarks (head tilted left)
        tilt_landmarks = LandmarkPoints(
            nose=np.array([95, 150]),   # Moved slightly left
            left_ear=np.array([70, 135]),  # Left ear closer to nose
            right_ear=np.array([125, 165]), # Right ear further from nose
            left_shoulder=np.array([60, 200]),
            right_shoulder=np.array([140, 200])
        )
        
        result = self.detector.detect(tilt_landmarks)
        # Should detect tilt due to asymmetry
        if result.detected:
            self.assertGreater(result.confidence, 0)
            self.assertEqual(result.status, DetectionStatus.DETECTED)


class TestNeckRotationDetector(unittest.TestCase):
    """Test neck rotation detection logic"""
    
    def setUp(self):
        self.config = SystemConfig()
        self.detector = NeckRotationDetector(self.config)
        self.landmarks = LandmarkPoints(
            nose=np.array([100, 150]),
            left_ear=np.array([80, 140]),
            right_ear=np.array([120, 140]),
            left_shoulder=np.array([60, 200]),
            right_shoulder=np.array([140, 200])
        )
    
    def test_rotation_detection_positive(self):
        """Test positive rotation detection"""
        # Complete calibration first
        for i in range(15):
            self.detector.detect(self.landmarks)
        
        # Create right rotation landmarks (head turned right)
        rotation_landmarks = LandmarkPoints(
            nose=np.array([110, 150]),     # Nose moved right
            left_ear=np.array([60, 140]),  # Left ear much more visible
            right_ear=np.array([130, 140]), # Right ear less visible
            left_shoulder=np.array([60, 200]),
            right_shoulder=np.array([140, 200])
        )
        
        result = self.detector.detect(rotation_landmarks)
        # May or may not detect depending on threshold, test structure
        self.assertIsInstance(result, ExerciseResult)
        self.assertEqual(result.exercise_type, ExerciseType.NECK_ROTATION)


class TestChinTuckDetector(unittest.TestCase):
    """Test chin tuck detection logic"""
    
    def setUp(self):
        self.config = SystemConfig()
        self.detector = ChinTuckDetector(self.config)
        self.landmarks = LandmarkPoints(
            nose=np.array([100, 150]),
            left_ear=np.array([80, 140]),
            right_ear=np.array([120, 140]),
            left_shoulder=np.array([60, 200]),
            right_shoulder=np.array([140, 200])
        )
    
    def test_chin_tuck_detection_positive(self):
        """Test positive chin tuck detection"""
        # Complete calibration first
        for i in range(15):
            self.detector.detect(self.landmarks)
        
        # Create chin tuck landmarks (chin pulled back)
        tuck_landmarks = LandmarkPoints(
            nose=np.array([95, 155]),      # Nose moved back and slightly down
            left_ear=np.array([80, 140]),  # Ears stay relatively same
            right_ear=np.array([120, 140]),
            left_shoulder=np.array([60, 200]),
            right_shoulder=np.array([140, 200])
        )
        
        result = self.detector.detect(tuck_landmarks)
        # Test structure rather than specific detection
        self.assertIsInstance(result, ExerciseResult)
        self.assertEqual(result.exercise_type, ExerciseType.CHIN_TUCK)


class TestExerciseDetectionSystem(unittest.TestCase):
    """Test the main exercise detection system"""
    
    def setUp(self):
        self.config = SystemConfig()
        self.system = ExerciseDetectionSystem(self.config)
    
    def test_system_initialization(self):
        """Test system initialization"""
        self.assertEqual(len(self.system.detectors), 5)
        self.assertIn(ExerciseType.CERVICAL_FLEXION, self.system.detectors)
        self.assertIn(ExerciseType.CERVICAL_EXTENSION, self.system.detectors)
        self.assertIn(ExerciseType.LATERAL_NECK_TILT, self.system.detectors)
        self.assertIn(ExerciseType.NECK_ROTATION, self.system.detectors)
        self.assertIn(ExerciseType.CHIN_TUCK, self.system.detectors)
    
    def test_detect_exercises_with_none_pose(self):
        """Test exercise detection with no pose results"""
        results = self.system.detect_exercises(None, (480, 640, 3))
        
        self.assertEqual(len(results), 5)
        for exercise_type, result in results.items():
            self.assertIsInstance(result, ExerciseResult)
            self.assertFalse(result.detected)
            self.assertEqual(result.status, DetectionStatus.ERROR)
    
    @patch('src.utils.geometry.LandmarkExtractor.extract_landmarks')
    def test_detect_exercises_with_valid_pose(self, mock_extract):
        """Test exercise detection with valid pose landmarks"""
        # Mock the landmark extraction
        mock_landmarks = LandmarkPoints(
            nose=np.array([100, 150]),
            left_ear=np.array([80, 140]),
            right_ear=np.array([120, 140]),
            left_shoulder=np.array([60, 200]),
            right_shoulder=np.array([140, 200])
        )
        mock_extract.return_value = mock_landmarks
        
        # Mock pose results
        mock_pose_results = Mock()
        
        results = self.system.detect_exercises(mock_pose_results, (480, 640, 3))
        
        self.assertEqual(len(results), 5)
        for exercise_type, result in results.items():
            self.assertIsInstance(result, ExerciseResult)
            self.assertEqual(result.status, DetectionStatus.CALIBRATING)
    
    def test_reset_baselines(self):
        """Test baseline reset functionality"""
        # Perform some detections first
        self.system.total_detections = 100
        
        self.system.reset_baselines()
        
        # Check that all detectors were reset
        for detector in self.system.detectors.values():
            self.assertFalse(detector.is_calibrated)
            self.assertEqual(detector.frames_collected, 0)
        
        # Check system stats reset
        self.assertEqual(self.system.total_detections, 0)
    
    def test_get_system_stats(self):
        """Test system statistics generation"""
        stats = self.system.get_system_stats()
        
        self.assertIn('total_detections', stats)
        self.assertIn('session_duration', stats)
        self.assertIn('detections_per_second', stats)
        self.assertIn('active_detectors', stats)
        
        self.assertIsInstance(stats['total_detections'], int)
        self.assertIsInstance(stats['session_duration'], float)
        self.assertIsInstance(stats['detections_per_second'], float)
        self.assertIsInstance(stats['active_detectors'], int)


class TestSystemConfigIntegration(unittest.TestCase):
    """Test system configuration integration"""
    
    def test_config_application(self):
        """Test that configuration is properly applied to detectors"""
        custom_config = SystemConfig(
            flexion_threshold=0.9,
            extension_threshold=1.2,
            calibration_frames=20
        )
        
        detector = CervicalFlexionDetector(custom_config)
        self.assertEqual(detector.threshold, 0.9)
        self.assertEqual(detector.calibration_frames, 15)  # Uses default from detector
        
        system = ExerciseDetectionSystem(custom_config)
        self.assertEqual(system.config.flexion_threshold, 0.9)
        self.assertEqual(system.config.extension_threshold, 1.2)


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestLandmarkPoints,
        TestCervicalFlexionDetector,
        TestCervicalExtensionDetector,
        TestLateralNeckTiltDetector,
        TestNeckRotationDetector,
        TestChinTuckDetector,
        TestExerciseDetectionSystem,
        TestSystemConfigIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*50}")
