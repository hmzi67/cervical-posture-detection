"""
Unit tests for geometry utilities and mathematical functions.

Tests cover:
- Distance and angle calculations
- Landmark extraction from MediaPipe results
- Mathematical utility functions
- Error handling for edge cases
"""
import unittest
import numpy as np
from unittest.mock import Mock, MagicMock
import sys
import os

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.utils.geometry import GeometryUtils, LandmarkExtractor, MathUtils
from src.core.models import LandmarkPoints


class TestGeometryUtils(unittest.TestCase):
    """Test geometric calculation utilities"""
    
    def setUp(self):
        self.point1 = np.array([0, 0])
        self.point2 = np.array([3, 4])
        self.point3 = np.array([0, 5])
    
    def test_calculate_distance(self):
        """Test Euclidean distance calculation"""
        distance = GeometryUtils.calculate_distance(self.point1, self.point2)
        self.assertAlmostEqual(distance, 5.0, places=2)
        
        # Test same point distance
        distance = GeometryUtils.calculate_distance(self.point1, self.point1)
        self.assertEqual(distance, 0.0)
        
        # Test negative coordinates
        point_neg = np.array([-3, -4])
        distance = GeometryUtils.calculate_distance(self.point1, point_neg)
        self.assertAlmostEqual(distance, 5.0, places=2)
    
    def test_calculate_angle(self):
        """Test angle calculation between three points"""
        # Right angle test (90 degrees)
        p1 = np.array([1, 0])
        p2 = np.array([0, 0])  # vertex
        p3 = np.array([0, 1])
        
        angle = GeometryUtils.calculate_angle(p1, p2, p3)
        self.assertAlmostEqual(angle, 90.0, places=1)
        
        # Straight line test (180 degrees)
        p1 = np.array([-1, 0])
        p2 = np.array([0, 0])
        p3 = np.array([1, 0])
        
        angle = GeometryUtils.calculate_angle(p1, p2, p3)
        self.assertAlmostEqual(angle, 180.0, places=1)
        
        # Acute angle test (~60 degrees)
        p1 = np.array([1, 0])
        p2 = np.array([0, 0])
        p3 = np.array([0.5, np.sqrt(3)/2])
        
        angle = GeometryUtils.calculate_angle(p1, p2, p3)
        self.assertAlmostEqual(angle, 60.0, places=1)
    
    def test_calculate_angle_edge_cases(self):
        """Test angle calculation edge cases"""
        # Zero-length vector case
        p1 = np.array([0, 0])
        p2 = np.array([0, 0])  # Same as p1
        p3 = np.array([1, 1])
        
        angle = GeometryUtils.calculate_angle(p1, p2, p3)
        self.assertEqual(angle, 0.0)
    
    def test_calculate_ratio(self):
        """Test ratio calculation with baseline"""
        ratio = GeometryUtils.calculate_ratio(10.0, 5.0)
        self.assertEqual(ratio, 2.0)
        
        ratio = GeometryUtils.calculate_ratio(3.0, 6.0)
        self.assertEqual(ratio, 0.5)
        
        # Edge case: zero baseline
        ratio = GeometryUtils.calculate_ratio(5.0, 0.0)
        self.assertEqual(ratio, 1.0)
        
        # Edge case: zero distance
        ratio = GeometryUtils.calculate_ratio(0.0, 5.0)
        self.assertEqual(ratio, 0.0)
    
    def test_smooth_value(self):
        """Test exponential smoothing function"""
        # Default smoothing factor (0.3)
        smoothed = GeometryUtils.smooth_value(10.0, 0.0)
        expected = 0.3 * 10.0 + 0.7 * 0.0
        self.assertAlmostEqual(smoothed, expected, places=2)
        
        # Custom smoothing factor
        smoothed = GeometryUtils.smooth_value(10.0, 0.0, 0.5)
        expected = 0.5 * 10.0 + 0.5 * 0.0
        self.assertAlmostEqual(smoothed, expected, places=2)
        
        # No smoothing (factor = 1.0)
        smoothed = GeometryUtils.smooth_value(10.0, 5.0, 1.0)
        self.assertEqual(smoothed, 10.0)
        
        # Full smoothing (factor = 0.0)
        smoothed = GeometryUtils.smooth_value(10.0, 5.0, 0.0)
        self.assertEqual(smoothed, 5.0)


class TestLandmarkExtractor(unittest.TestCase):
    """Test landmark extraction from MediaPipe results"""
    
    def setUp(self):
        self.frame_shape = (480, 640, 3)  # height, width, channels
        
        # Create mock MediaPipe landmarks
        self.mock_landmark = Mock()
        self.mock_landmark.x = 0.5  # Normalized coordinates
        self.mock_landmark.y = 0.25
        
        # Create mock pose results
        self.mock_pose_results = Mock()
        self.mock_pose_results.pose_landmarks = Mock()
        
        # Mock landmarks list with required indices
        mock_landmarks = []
        landmark_positions = [
            (0.5, 0.25),    # 0: nose
            (0.0, 0.0),     # 1: left_eye_inner
            (0.0, 0.0),     # 2: left_eye
            (0.0, 0.0),     # 3: left_eye_outer
            (0.0, 0.0),     # 4: right_eye_inner
            (0.0, 0.0),     # 5: right_eye
            (0.0, 0.0),     # 6: right_eye_outer
            (0.4, 0.2),     # 7: left_ear
            (0.6, 0.2),     # 8: right_ear
            (0.0, 0.0),     # 9: mouth_left
            (0.0, 0.0),     # 10: mouth_right
            (0.3, 0.6),     # 11: left_shoulder
            (0.7, 0.6),     # 12: right_shoulder
        ]
        
        for x, y in landmark_positions:
            landmark = Mock()
            landmark.x = x
            landmark.y = y
            mock_landmarks.append(landmark)
        
        # Add more landmarks to reach required indices
        for i in range(len(landmark_positions), 33):
            landmark = Mock()
            landmark.x = 0.5
            landmark.y = 0.5
            mock_landmarks.append(landmark)
        
        self.mock_pose_results.pose_landmarks.landmark = mock_landmarks
    
    def test_extract_landmarks_success(self):
        """Test successful landmark extraction"""
        landmarks = LandmarkExtractor.extract_landmarks(self.mock_pose_results, self.frame_shape)
        
        self.assertIsNotNone(landmarks)
        self.assertIsInstance(landmarks, LandmarkPoints)
        
        # Check coordinate conversion (normalized to pixel coordinates)
        expected_nose_x = 0.5 * 640  # width
        expected_nose_y = 0.25 * 480  # height
        
        self.assertAlmostEqual(landmarks.nose[0], expected_nose_x, places=1)
        self.assertAlmostEqual(landmarks.nose[1], expected_nose_y, places=1)
        
        # Check all required landmarks exist
        self.assertIsInstance(landmarks.left_ear, np.ndarray)
        self.assertIsInstance(landmarks.right_ear, np.ndarray)
        self.assertIsInstance(landmarks.left_shoulder, np.ndarray)
        self.assertIsInstance(landmarks.right_shoulder, np.ndarray)
    
    def test_extract_landmarks_no_pose(self):
        """Test landmark extraction with no pose detected"""
        mock_pose_no_landmarks = Mock()
        mock_pose_no_landmarks.pose_landmarks = None
        
        landmarks = LandmarkExtractor.extract_landmarks(mock_pose_no_landmarks, self.frame_shape)
        
        self.assertIsNone(landmarks)
    
    def test_extract_landmarks_missing_landmarks(self):
        """Test landmark extraction with missing landmarks"""
        # Create pose results with insufficient landmarks
        mock_pose_incomplete = Mock()
        mock_pose_incomplete.pose_landmarks = Mock()
        mock_pose_incomplete.pose_landmarks.landmark = [Mock() for _ in range(5)]  # Only 5 landmarks
        
        landmarks = LandmarkExtractor.extract_landmarks(mock_pose_incomplete, self.frame_shape)
        
        self.assertIsNone(landmarks)
    
    def test_is_pose_visible(self):
        """Test pose visibility validation"""
        # Valid landmarks
        valid_landmarks = LandmarkPoints(
            nose=np.array([100, 150]),
            left_ear=np.array([80, 140]),
            right_ear=np.array([120, 140]),
            left_shoulder=np.array([60, 200]),
            right_shoulder=np.array([140, 200])
        )
        
        self.assertTrue(LandmarkExtractor.is_pose_visible(valid_landmarks))
        
        # Invalid landmarks (negative coordinates)
        invalid_landmarks = LandmarkPoints(
            nose=np.array([-10, 150]),  # Negative x
            left_ear=np.array([80, 140]),
            right_ear=np.array([120, 140]),
            left_shoulder=np.array([60, 200]),
            right_shoulder=np.array([140, 200])
        )
        
        self.assertFalse(LandmarkExtractor.is_pose_visible(invalid_landmarks))
        
        # Invalid landmarks (NaN values)
        nan_landmarks = LandmarkPoints(
            nose=np.array([np.nan, 150]),
            left_ear=np.array([80, 140]),
            right_ear=np.array([120, 140]),
            left_shoulder=np.array([60, 200]),
            right_shoulder=np.array([140, 200])
        )
        
        self.assertFalse(LandmarkExtractor.is_pose_visible(nan_landmarks))


class TestMathUtils(unittest.TestCase):
    """Test mathematical utility functions"""
    
    def test_normalize_angle(self):
        """Test angle normalization to 0-360 range"""
        self.assertEqual(MathUtils.normalize_angle(0), 0)
        self.assertEqual(MathUtils.normalize_angle(180), 180)
        self.assertEqual(MathUtils.normalize_angle(360), 0)
        self.assertEqual(MathUtils.normalize_angle(450), 90)
        self.assertEqual(MathUtils.normalize_angle(-90), 270)
        self.assertEqual(MathUtils.normalize_angle(-450), 270)
    
    def test_clamp(self):
        """Test value clamping to specified range"""
        # Value within range
        self.assertEqual(MathUtils.clamp(5, 0, 10), 5)
        
        # Value below minimum
        self.assertEqual(MathUtils.clamp(-5, 0, 10), 0)
        
        # Value above maximum
        self.assertEqual(MathUtils.clamp(15, 0, 10), 10)
        
        # Edge cases
        self.assertEqual(MathUtils.clamp(0, 0, 10), 0)
        self.assertEqual(MathUtils.clamp(10, 0, 10), 10)
        
        # Reversed range (should still work)
        self.assertEqual(MathUtils.clamp(5, 10, 0), 5)  # Clamps to max
    
    def test_map_range(self):
        """Test value mapping from one range to another"""
        # Basic mapping
        result = MathUtils.map_range(5, 0, 10, 0, 100)
        self.assertEqual(result, 50)
        
        # Reverse mapping
        result = MathUtils.map_range(25, 0, 100, 10, 0)
        self.assertEqual(result, 7.5)
        
        # Identity mapping
        result = MathUtils.map_range(5, 0, 10, 0, 10)
        self.assertEqual(result, 5)
        
        # Zero-width source range
        result = MathUtils.map_range(5, 5, 5, 0, 100)
        self.assertEqual(result, 0)  # Should return to_min
        
        # Negative ranges
        result = MathUtils.map_range(-5, -10, 0, 0, 100)
        self.assertEqual(result, 50)


class TestGeometryIntegration(unittest.TestCase):
    """Test integration between geometry components"""
    
    def test_landmark_to_distance_calculation(self):
        """Test complete pipeline from landmarks to distance"""
        landmarks = LandmarkPoints(
            nose=np.array([100, 150]),
            left_ear=np.array([80, 140]),
            right_ear=np.array([120, 140]),
            left_shoulder=np.array([60, 200]),
            right_shoulder=np.array([140, 200])
        )
        
        # Calculate distances as done in detectors
        mid_shoulder = (landmarks.left_shoulder + landmarks.right_shoulder) / 2
        nose_to_shoulder_distance = GeometryUtils.calculate_distance(landmarks.nose, mid_shoulder)
        
        self.assertIsInstance(nose_to_shoulder_distance, (int, float))
        self.assertGreater(nose_to_shoulder_distance, 0)
        
        # Test ear distances
        left_ear_distance = GeometryUtils.calculate_distance(landmarks.nose, landmarks.left_ear)
        right_ear_distance = GeometryUtils.calculate_distance(landmarks.nose, landmarks.right_ear)
        
        self.assertIsInstance(left_ear_distance, (int, float))
        self.assertIsInstance(right_ear_distance, (int, float))
    
    def test_coordinate_system_consistency(self):
        """Test coordinate system consistency across calculations"""
        # Create landmarks in different coordinate systems
        landmarks_pixels = LandmarkPoints(
            nose=np.array([320, 240]),  # Center of 640x480 image
            left_ear=np.array([300, 220]),
            right_ear=np.array([340, 220]),
            left_shoulder=np.array([280, 300]),
            right_shoulder=np.array([360, 300])
        )
        
        landmarks_normalized = LandmarkPoints(
            nose=np.array([0.5, 0.5]),  # Normalized coordinates
            left_ear=np.array([0.46875, 0.4583]),
            right_ear=np.array([0.53125, 0.4583]),
            left_shoulder=np.array([0.4375, 0.625]),
            right_shoulder=np.array([0.5625, 0.625])
        )
        
        # Distances should be proportional
        pixel_distance = GeometryUtils.calculate_distance(
            landmarks_pixels.nose, landmarks_pixels.left_ear
        )
        normalized_distance = GeometryUtils.calculate_distance(
            landmarks_normalized.nose, landmarks_normalized.left_ear
        )
        
        self.assertGreater(pixel_distance, normalized_distance)
        
        # Ratios should be similar regardless of coordinate system
        pixel_mid_shoulder = (landmarks_pixels.left_shoulder + landmarks_pixels.right_shoulder) / 2
        normalized_mid_shoulder = (landmarks_normalized.left_shoulder + landmarks_normalized.right_shoulder) / 2
        
        pixel_nose_shoulder = GeometryUtils.calculate_distance(landmarks_pixels.nose, pixel_mid_shoulder)
        normalized_nose_shoulder = GeometryUtils.calculate_distance(landmarks_normalized.nose, normalized_mid_shoulder)
        
        pixel_ratio = GeometryUtils.calculate_ratio(pixel_distance, pixel_nose_shoulder)
        normalized_ratio = GeometryUtils.calculate_ratio(normalized_distance, normalized_nose_shoulder)
        
        self.assertAlmostEqual(pixel_ratio, normalized_ratio, places=2)


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestGeometryUtils,
        TestLandmarkExtractor,
        TestMathUtils,
        TestGeometryIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Geometry Utilities Test Results")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*50}")
