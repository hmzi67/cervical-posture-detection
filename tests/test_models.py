"""
Unit tests for data models and configuration classes.

Tests cover:
- Data model creation and validation
- Enum functionality and values
- Configuration parameter handling
- Serialization and deserialization
- Edge cases and error handling
"""
import unittest
import time
import numpy as np
import sys
import os

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.core.models import (
    ExerciseType, DetectionStatus, LandmarkPoints, ExerciseResult,
    CalibrationState, SystemConfig
)


class TestExerciseType(unittest.TestCase):
    """Test ExerciseType enumeration"""
    
    def test_exercise_type_values(self):
        """Test that all exercise types have correct values"""
        expected_values = {
            ExerciseType.CERVICAL_FLEXION: "Cervical Flexion (Chin-to-chest)",
            ExerciseType.CERVICAL_EXTENSION: "Cervical Extension (Look upward)",
            ExerciseType.LATERAL_NECK_TILT: "Lateral Neck Tilt (Left and Right)",
            ExerciseType.NECK_ROTATION: "Neck Rotation (Turn head left/right)",
            ExerciseType.CHIN_TUCK: "Chin Tuck (Retract chin)"
        }
        
        for exercise_type, expected_value in expected_values.items():
            self.assertEqual(exercise_type.value, expected_value)
    
    def test_exercise_type_count(self):
        """Test that we have exactly 5 exercise types"""
        self.assertEqual(len(list(ExerciseType)), 5)
    
    def test_exercise_type_uniqueness(self):
        """Test that all exercise type values are unique"""
        values = [exercise_type.value for exercise_type in ExerciseType]
        self.assertEqual(len(values), len(set(values)))


class TestDetectionStatus(unittest.TestCase):
    """Test DetectionStatus enumeration"""
    
    def test_detection_status_values(self):
        """Test that all detection statuses have correct values"""
        expected_values = {
            DetectionStatus.CALIBRATING: "calibrating",
            DetectionStatus.READY: "ready",
            DetectionStatus.DETECTED: "detected",
            DetectionStatus.NOT_DETECTED: "not_detected",
            DetectionStatus.ERROR: "error"
        }
        
        for status, expected_value in expected_values.items():
            self.assertEqual(status.value, expected_value)
    
    def test_detection_status_count(self):
        """Test that we have exactly 5 detection statuses"""
        self.assertEqual(len(list(DetectionStatus)), 5)


class TestLandmarkPoints(unittest.TestCase):
    """Test LandmarkPoints data class"""
    
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
        self.assertIsInstance(self.landmarks.left_ear, np.ndarray)
        self.assertIsInstance(self.landmarks.right_ear, np.ndarray)
        self.assertIsInstance(self.landmarks.left_shoulder, np.ndarray)
        self.assertIsInstance(self.landmarks.right_shoulder, np.ndarray)
    
    def test_landmark_coordinates(self):
        """Test landmark coordinate values"""
        self.assertEqual(self.landmarks.nose[0], 100)
        self.assertEqual(self.landmarks.nose[1], 150)
        self.assertEqual(self.landmarks.left_ear[0], 80)
        self.assertEqual(self.landmarks.left_ear[1], 140)
    
    def test_landmark_array_properties(self):
        """Test that landmarks are proper numpy arrays"""
        for landmark in [self.landmarks.nose, self.landmarks.left_ear, 
                        self.landmarks.right_ear, self.landmarks.left_shoulder, 
                        self.landmarks.right_shoulder]:
            self.assertEqual(len(landmark), 2)  # Should be 2D coordinates
            self.assertTrue(np.isfinite(landmark).all())  # Should be finite numbers


class TestExerciseResult(unittest.TestCase):
    """Test ExerciseResult data class"""
    
    def setUp(self):
        self.result = ExerciseResult(
            exercise_type=ExerciseType.CERVICAL_FLEXION,
            detected=True,
            confidence=0.85,
            status=DetectionStatus.DETECTED,
            status_message="Exercise detected successfully",
            metrics={'distance_ratio': 0.7, 'threshold': 0.85},
            timestamp=time.time()
        )
    
    def test_result_creation(self):
        """Test exercise result creation"""
        self.assertEqual(self.result.exercise_type, ExerciseType.CERVICAL_FLEXION)
        self.assertTrue(self.result.detected)
        self.assertEqual(self.result.confidence, 0.85)
        self.assertEqual(self.result.status, DetectionStatus.DETECTED)
        self.assertEqual(self.result.status_message, "Exercise detected successfully")
        self.assertIsInstance(self.result.metrics, dict)
        self.assertIsInstance(self.result.timestamp, float)
    
    def test_result_to_dict(self):
        """Test result serialization to dictionary"""
        result_dict = self.result.to_dict()
        
        expected_keys = ['exercise_type', 'detected', 'confidence', 'status', 
                        'status_message', 'metrics', 'timestamp']
        
        for key in expected_keys:
            self.assertIn(key, result_dict)
        
        self.assertEqual(result_dict['exercise_type'], ExerciseType.CERVICAL_FLEXION.value)
        self.assertTrue(result_dict['detected'])
        self.assertEqual(result_dict['confidence'], 0.85)
        self.assertEqual(result_dict['status'], DetectionStatus.DETECTED.value)
    
    def test_result_minimal_creation(self):
        """Test result creation with minimal parameters"""
        minimal_result = ExerciseResult(
            exercise_type=ExerciseType.CHIN_TUCK,
            detected=False,
            confidence=0.0,
            status=DetectionStatus.NOT_DETECTED
        )
        
        self.assertEqual(minimal_result.exercise_type, ExerciseType.CHIN_TUCK)
        self.assertFalse(minimal_result.detected)
        self.assertEqual(minimal_result.confidence, 0.0)
        self.assertEqual(minimal_result.status, DetectionStatus.NOT_DETECTED)
        self.assertEqual(minimal_result.status_message, "")
        self.assertIsNone(minimal_result.metrics)
        self.assertIsNone(minimal_result.timestamp)
    
    def test_result_with_none_metrics(self):
        """Test result handling with None metrics"""
        result = ExerciseResult(
            exercise_type=ExerciseType.NECK_ROTATION,
            detected=False,
            confidence=0.0,
            status=DetectionStatus.ERROR,
            metrics=None
        )
        
        result_dict = result.to_dict()
        self.assertEqual(result_dict['metrics'], {})


class TestCalibrationState(unittest.TestCase):
    """Test CalibrationState data class"""
    
    def setUp(self):
        self.calibration = CalibrationState()
    
    def test_initial_state(self):
        """Test initial calibration state"""
        self.assertEqual(self.calibration.frames_collected, 0)
        self.assertEqual(self.calibration.frames_required, 15)
        self.assertIsNone(self.calibration.baseline_values)
        self.assertFalse(self.calibration.is_complete)
    
    def test_progress_percentage(self):
        """Test progress percentage calculation"""
        # Initial progress
        self.assertEqual(self.calibration.progress_percentage, 0.0)
        
        # Partial progress
        self.calibration.frames_collected = 7
        expected_progress = (7 / 15) * 100
        self.assertAlmostEqual(self.calibration.progress_percentage, expected_progress, places=1)
        
        # Complete progress
        self.calibration.frames_collected = 15
        self.assertEqual(self.calibration.progress_percentage, 100.0)
        
        # Over-complete progress (should be capped at 100%)
        self.calibration.frames_collected = 20
        self.assertEqual(self.calibration.progress_percentage, 100.0)
    
    def test_reset_functionality(self):
        """Test calibration reset"""
        # Set up some state
        self.calibration.frames_collected = 10
        self.calibration.baseline_values = {'test': 123}
        self.calibration.is_complete = True
        
        # Reset
        self.calibration.reset()
        
        # Check reset state
        self.assertEqual(self.calibration.frames_collected, 0)
        self.assertIsNone(self.calibration.baseline_values)
        self.assertFalse(self.calibration.is_complete)
    
    def test_custom_frames_required(self):
        """Test calibration with custom frames required"""
        custom_calibration = CalibrationState(frames_required=20)
        
        self.assertEqual(custom_calibration.frames_required, 20)
        
        custom_calibration.frames_collected = 10
        expected_progress = (10 / 20) * 100
        self.assertAlmostEqual(custom_calibration.progress_percentage, expected_progress, places=1)


class TestSystemConfig(unittest.TestCase):
    """Test SystemConfig data class"""
    
    def test_default_config(self):
        """Test default configuration values"""
        config = SystemConfig()
        
        # Detection thresholds
        self.assertEqual(config.flexion_threshold, 0.85)
        self.assertEqual(config.extension_threshold, 1.15)
        self.assertEqual(config.tilt_threshold, 0.15)
        self.assertEqual(config.rotation_threshold, 1.5)
        self.assertEqual(config.chin_tuck_threshold, 0.8)
        
        # Calibration settings
        self.assertEqual(config.calibration_frames, 15)
        self.assertEqual(config.confidence_smoothing, 0.3)
        
        # Performance settings
        self.assertEqual(config.min_detection_confidence, 0.5)
        self.assertEqual(config.min_tracking_confidence, 0.5)
        self.assertEqual(config.model_complexity, 1)
        
        # UI settings
        self.assertEqual(config.fps_limit, 15)
        self.assertEqual(config.video_width, 640)
        self.assertEqual(config.video_height, 480)
    
    def test_custom_config(self):
        """Test custom configuration values"""
        config = SystemConfig(
            flexion_threshold=0.9,
            extension_threshold=1.2,
            calibration_frames=20,
            fps_limit=25,
            video_width=1280,
            video_height=720
        )
        
        self.assertEqual(config.flexion_threshold, 0.9)
        self.assertEqual(config.extension_threshold, 1.2)
        self.assertEqual(config.calibration_frames, 20)
        self.assertEqual(config.fps_limit, 25)
        self.assertEqual(config.video_width, 1280)
        self.assertEqual(config.video_height, 720)
    
    def test_config_validation_ranges(self):
        """Test configuration value ranges make sense"""
        config = SystemConfig()
        
        # Thresholds should be positive
        self.assertGreater(config.flexion_threshold, 0)
        self.assertGreater(config.extension_threshold, 0)
        self.assertGreater(config.tilt_threshold, 0)
        self.assertGreater(config.rotation_threshold, 0)
        self.assertGreater(config.chin_tuck_threshold, 0)
        
        # Confidence values should be between 0 and 1
        self.assertGreaterEqual(config.min_detection_confidence, 0)
        self.assertLessEqual(config.min_detection_confidence, 1)
        self.assertGreaterEqual(config.min_tracking_confidence, 0)
        self.assertLessEqual(config.min_tracking_confidence, 1)
        self.assertGreaterEqual(config.confidence_smoothing, 0)
        self.assertLessEqual(config.confidence_smoothing, 1)
        
        # Video dimensions should be positive
        self.assertGreater(config.video_width, 0)
        self.assertGreater(config.video_height, 0)
        self.assertGreater(config.fps_limit, 0)
        
        # Calibration frames should be positive
        self.assertGreater(config.calibration_frames, 0)


class TestModelIntegration(unittest.TestCase):
    """Test integration between different model classes"""
    
    def test_exercise_result_with_all_exercise_types(self):
        """Test creating exercise results for all exercise types"""
        for exercise_type in ExerciseType:
            result = ExerciseResult(
                exercise_type=exercise_type,
                detected=True,
                confidence=0.8,
                status=DetectionStatus.DETECTED
            )
            
            self.assertEqual(result.exercise_type, exercise_type)
            self.assertTrue(result.detected)
    
    def test_exercise_result_with_all_statuses(self):
        """Test creating exercise results with all status types"""
        for status in DetectionStatus:
            result = ExerciseResult(
                exercise_type=ExerciseType.CERVICAL_FLEXION,
                detected=(status == DetectionStatus.DETECTED),
                confidence=0.5 if status == DetectionStatus.DETECTED else 0.0,
                status=status
            )
            
            self.assertEqual(result.status, status)
            if status == DetectionStatus.DETECTED:
                self.assertTrue(result.detected)
            else:
                self.assertFalse(result.detected)
    
    def test_config_with_calibration_state(self):
        """Test configuration integration with calibration state"""
        config = SystemConfig(calibration_frames=20)
        calibration = CalibrationState(frames_required=config.calibration_frames)
        
        self.assertEqual(calibration.frames_required, config.calibration_frames)
        
        # Test progress calculation with config values
        calibration.frames_collected = config.calibration_frames // 2
        self.assertEqual(calibration.progress_percentage, 50.0)
    
    def test_landmark_points_with_numpy_operations(self):
        """Test landmark points with numpy operations"""
        landmarks = LandmarkPoints(
            nose=np.array([100.0, 150.0]),
            left_ear=np.array([80.0, 140.0]),
            right_ear=np.array([120.0, 140.0]),
            left_shoulder=np.array([60.0, 200.0]),
            right_shoulder=np.array([140.0, 200.0])
        )
        
        # Test midpoint calculation (common operation)
        mid_shoulder = (landmarks.left_shoulder + landmarks.right_shoulder) / 2
        expected_mid = np.array([100.0, 200.0])
        
        np.testing.assert_array_equal(mid_shoulder, expected_mid)
        
        # Test that landmarks can be used in calculations
        mid_ear = (landmarks.left_ear + landmarks.right_ear) / 2
        self.assertEqual(mid_ear[0], 100.0)
        self.assertEqual(mid_ear[1], 140.0)


class TestDataValidation(unittest.TestCase):
    """Test data validation and error handling"""
    
    def test_confidence_bounds(self):
        """Test confidence value bounds handling"""
        # Valid confidence values
        result = ExerciseResult(
            exercise_type=ExerciseType.CERVICAL_FLEXION,
            detected=True,
            confidence=0.85,
            status=DetectionStatus.DETECTED
        )
        self.assertEqual(result.confidence, 0.85)
        
        # Edge case: zero confidence
        result_zero = ExerciseResult(
            exercise_type=ExerciseType.CERVICAL_FLEXION,
            detected=False,
            confidence=0.0,
            status=DetectionStatus.NOT_DETECTED
        )
        self.assertEqual(result_zero.confidence, 0.0)
        
        # Edge case: maximum confidence
        result_max = ExerciseResult(
            exercise_type=ExerciseType.CERVICAL_FLEXION,
            detected=True,
            confidence=1.0,
            status=DetectionStatus.DETECTED
        )
        self.assertEqual(result_max.confidence, 1.0)
    
    def test_timestamp_handling(self):
        """Test timestamp handling in exercise results"""
        current_time = time.time()
        
        result = ExerciseResult(
            exercise_type=ExerciseType.NECK_ROTATION,
            detected=True,
            confidence=0.9,
            status=DetectionStatus.DETECTED,
            timestamp=current_time
        )
        
        self.assertEqual(result.timestamp, current_time)
        
        # Test serialization with timestamp
        result_dict = result.to_dict()
        self.assertEqual(result_dict['timestamp'], current_time)


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestExerciseType,
        TestDetectionStatus,
        TestLandmarkPoints,
        TestExerciseResult,
        TestCalibrationState,
        TestSystemConfig,
        TestModelIntegration,
        TestDataValidation
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Data Models Test Results")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*50}")
