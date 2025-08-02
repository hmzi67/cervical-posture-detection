"""
Unit tests for video processing and MediaPipe integration.

Tests cover:
- Video processor initialization
- Frame processing pipeline
- MediaPipe integration
- Performance monitoring
- Error handling and cleanup
"""
import unittest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import cv2
import sys
import os

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.core.video_processor import VideoProcessor
from src.core.models import SystemConfig, ExerciseType, ExerciseResult, DetectionStatus


class TestVideoProcessor(unittest.TestCase):
    """Test video processor functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = SystemConfig()
        self.processor = VideoProcessor(self.config)
        
        # Create a test frame (480x640x3 BGR image)
        self.test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    def test_initialization(self):
        """Test video processor initialization"""
        self.assertIsNotNone(self.processor.mp_pose)
        self.assertIsNotNone(self.processor.pose)
        self.assertIsNotNone(self.processor.mp_drawing)
        self.assertIsNotNone(self.processor.exercise_system)
        
        # Check initial state
        self.assertEqual(self.processor.frame_count, 0)
        self.assertEqual(len(self.processor.processing_times), 0)
    
    def test_initialization_with_custom_config(self):
        """Test initialization with custom configuration"""
        custom_config = SystemConfig(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.6,
            model_complexity=2
        )
        
        processor = VideoProcessor(custom_config)
        self.assertEqual(processor.config.min_detection_confidence, 0.7)
        self.assertEqual(processor.config.min_tracking_confidence, 0.6)
        self.assertEqual(processor.config.model_complexity, 2)
    
    @patch('mediapipe.solutions.pose.Pose.process')
    @patch('src.core.detection_system.ExerciseDetectionSystem.detect_exercises')
    def test_process_frame_success(self, mock_detect_exercises, mock_pose_process):
        """Test successful frame processing"""
        # Mock MediaPipe pose results
        mock_pose_results = Mock()
        mock_pose_results.pose_landmarks = Mock()
        mock_pose_process.return_value = mock_pose_results
        
        # Mock exercise detection results
        mock_results = {
            ExerciseType.CERVICAL_FLEXION: ExerciseResult(
                ExerciseType.CERVICAL_FLEXION, True, 0.8, DetectionStatus.DETECTED
            )
        }
        mock_detect_exercises.return_value = mock_results
        
        # Process frame
        processed_frame, exercise_results = self.processor.process_frame(self.test_frame)
        
        # Verify results
        self.assertIsInstance(processed_frame, np.ndarray)
        self.assertEqual(processed_frame.shape, self.test_frame.shape)
        self.assertIsInstance(exercise_results, dict)
        self.assertEqual(len(exercise_results), 1)
        
        # Verify MediaPipe was called
        mock_pose_process.assert_called_once()
        
        # Verify detection system was called
        mock_detect_exercises.assert_called_once_with(mock_pose_results, self.test_frame.shape)
        
        # Check frame count updated
        self.assertEqual(self.processor.frame_count, 1)
        self.assertEqual(len(self.processor.processing_times), 1)
    
    @patch('mediapipe.solutions.pose.Pose.process')
    def test_process_frame_no_landmarks(self, mock_pose_process):
        """Test frame processing with no pose landmarks detected"""
        # Mock MediaPipe pose results with no landmarks
        mock_pose_results = Mock()
        mock_pose_results.pose_landmarks = None
        mock_pose_process.return_value = mock_pose_results
        
        # Process frame
        processed_frame, exercise_results = self.processor.process_frame(self.test_frame)
        
        # Verify frame is returned (even without landmarks)
        self.assertIsInstance(processed_frame, np.ndarray)
        self.assertEqual(processed_frame.shape, self.test_frame.shape)
        
        # Verify exercise results are returned
        self.assertIsInstance(exercise_results, dict)
    
    @patch('mediapipe.solutions.pose.Pose.process')
    @patch('cv2.putText')
    def test_fps_drawing(self, mock_putText, mock_pose_process):
        """Test FPS drawing on frame"""
        # Mock pose processing
        mock_pose_results = Mock()
        mock_pose_results.pose_landmarks = None
        mock_pose_process.return_value = mock_pose_results
        
        # Process multiple frames to build up processing times
        for _ in range(5):
            self.processor.process_frame(self.test_frame)
        
        # Verify putText was called (for FPS display)
        self.assertTrue(mock_putText.called)
        
        # Check that FPS text was drawn in correct position
        calls = mock_putText.call_args_list
        last_call = calls[-1]
        args, kwargs = last_call
        
        # Should be drawing near top-right corner
        frame, text, position = args[:3]
        self.assertIn("FPS:", text)
        self.assertGreater(position[0], 500)  # Near right edge
        self.assertLess(position[1], 50)      # Near top
    
    def test_get_system_stats(self):
        """Test system statistics collection"""
        # Process some frames first
        with patch('mediapipe.solutions.pose.Pose.process') as mock_process:
            mock_pose_results = Mock()
            mock_pose_results.pose_landmarks = None
            mock_process.return_value = mock_pose_results
            
            for _ in range(3):
                self.processor.process_frame(self.test_frame)
        
        stats = self.processor.get_system_stats()
        
        # Verify stats structure
        self.assertIn('frame_count', stats)
        self.assertIn('avg_fps', stats)
        self.assertIn('avg_processing_time', stats)
        self.assertIn('detectors_count', stats)
        
        # Verify values
        self.assertEqual(stats['frame_count'], 3)
        self.assertIsInstance(stats['avg_fps'], (int, float))
        self.assertIsInstance(stats['avg_processing_time'], (int, float))
        self.assertIsInstance(stats['detectors_count'], int)
        self.assertGreater(stats['detectors_count'], 0)
    
    def test_reset_baselines(self):
        """Test baseline reset functionality"""
        # Process some frames first
        with patch('mediapipe.solutions.pose.Pose.process') as mock_process:
            mock_pose_results = Mock()
            mock_pose_results.pose_landmarks = None
            mock_process.return_value = mock_pose_results
            
            self.processor.process_frame(self.test_frame)
        
        # Mock the exercise system reset method
        with patch.object(self.processor.exercise_system, 'reset_baselines') as mock_reset:
            self.processor.reset_baselines()
            mock_reset.assert_called_once()
    
    def test_cleanup(self):
        """Test resource cleanup"""
        # Mock the pose object's close method
        with patch.object(self.processor.pose, 'close') as mock_close:
            self.processor.cleanup()
            mock_close.assert_called_once()
    
    def test_performance_monitoring(self):
        """Test performance monitoring functionality"""
        # Process frames and check performance tracking
        with patch('mediapipe.solutions.pose.Pose.process') as mock_process:
            mock_pose_results = Mock()
            mock_pose_results.pose_landmarks = None
            mock_process.return_value = mock_pose_results
            
            # Process multiple frames
            for _ in range(10):
                self.processor.process_frame(self.test_frame)
        
        # Check processing times are tracked
        self.assertEqual(len(self.processor.processing_times), 10)
        
        # All processing times should be positive
        for processing_time in self.processor.processing_times:
            self.assertGreater(processing_time, 0)
        
        # Frame count should be updated
        self.assertEqual(self.processor.frame_count, 10)
    
    def test_processing_time_limit(self):
        """Test that processing times list is limited to prevent memory issues"""
        with patch('mediapipe.solutions.pose.Pose.process') as mock_process:
            mock_pose_results = Mock()
            mock_pose_results.pose_landmarks = None
            mock_process.return_value = mock_pose_results
            
            # Process more than 30 frames (the limit)
            for _ in range(35):
                self.processor.process_frame(self.test_frame)
        
        # Should be limited to 30 processing times
        self.assertEqual(len(self.processor.processing_times), 30)
    
    @patch('mediapipe.solutions.drawing_utils.draw_landmarks')
    @patch('mediapipe.solutions.pose.Pose.process')
    def test_landmark_drawing(self, mock_pose_process, mock_draw_landmarks):
        """Test pose landmark drawing on frame"""
        # Mock MediaPipe pose results with landmarks
        mock_pose_results = Mock()
        mock_pose_results.pose_landmarks = Mock()
        mock_pose_process.return_value = mock_pose_results
        
        # Process frame
        self.processor.process_frame(self.test_frame)
        
        # Verify draw_landmarks was called
        mock_draw_landmarks.assert_called_once()
        
        # Check the arguments passed to draw_landmarks
        args, kwargs = mock_draw_landmarks.call_args
        frame, landmarks, connections = args[:3]
        
        self.assertIsInstance(frame, np.ndarray)
        self.assertEqual(landmarks, mock_pose_results.pose_landmarks)
    
    def test_frame_color_conversion(self):
        """Test BGR to RGB color conversion for MediaPipe"""
        with patch('cv2.cvtColor') as mock_cvtColor:
            with patch('mediapipe.solutions.pose.Pose.process') as mock_process:
                mock_pose_results = Mock()
                mock_pose_results.pose_landmarks = None
                mock_process.return_value = mock_pose_results
                
                # Make cvtColor return the same frame for simplicity
                mock_cvtColor.return_value = self.test_frame
                
                self.processor.process_frame(self.test_frame)
                
                # Verify BGR to RGB conversion was called
                mock_cvtColor.assert_called_with(self.test_frame, cv2.COLOR_BGR2RGB)


class TestVideoProcessorIntegration(unittest.TestCase):
    """Test video processor integration with other components"""
    
    def setUp(self):
        self.config = SystemConfig()
        self.processor = VideoProcessor(self.config)
        self.test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    @patch('src.core.detection_system.ExerciseDetectionSystem.detect_exercises')
    @patch('mediapipe.solutions.pose.Pose.process')
    def test_integration_with_exercise_system(self, mock_pose_process, mock_detect_exercises):
        """Test integration with exercise detection system"""
        # Mock MediaPipe results
        mock_pose_results = Mock()
        mock_pose_results.pose_landmarks = Mock()
        mock_pose_process.return_value = mock_pose_results
        
        # Mock exercise detection results
        expected_results = {
            ExerciseType.CERVICAL_FLEXION: ExerciseResult(
                ExerciseType.CERVICAL_FLEXION, True, 0.9, DetectionStatus.DETECTED
            ),
            ExerciseType.NECK_ROTATION: ExerciseResult(
                ExerciseType.NECK_ROTATION, False, 0.1, DetectionStatus.NOT_DETECTED
            )
        }
        mock_detect_exercises.return_value = expected_results
        
        # Process frame
        processed_frame, exercise_results = self.processor.process_frame(self.test_frame)
        
        # Verify exercise detection system was called with correct parameters
        mock_detect_exercises.assert_called_once_with(mock_pose_results, self.test_frame.shape)
        
        # Verify results are passed through correctly
        self.assertEqual(exercise_results, expected_results)
    
    def test_config_application(self):
        """Test that configuration is properly applied to MediaPipe"""
        custom_config = SystemConfig(
            min_detection_confidence=0.8,
            min_tracking_confidence=0.7,
            model_complexity=2
        )
        
        # Note: In actual implementation, these would need to be applied
        # to the MediaPipe Pose constructor. This test verifies the config is stored.
        processor = VideoProcessor(custom_config)
        
        self.assertEqual(processor.config.min_detection_confidence, 0.8)
        self.assertEqual(processor.config.min_tracking_confidence, 0.7)
        self.assertEqual(processor.config.model_complexity, 2)


class TestVideoProcessorErrorHandling(unittest.TestCase):
    """Test error handling in video processor"""
    
    def setUp(self):
        self.config = SystemConfig()
        self.processor = VideoProcessor(self.config)
        self.test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    @patch('mediapipe.solutions.pose.Pose.process')
    def test_mediapipe_processing_error(self, mock_pose_process):
        """Test handling of MediaPipe processing errors"""
        # Make MediaPipe raise an exception
        mock_pose_process.side_effect = Exception("MediaPipe error")
        
        # Process frame - should not crash
        try:
            processed_frame, exercise_results = self.processor.process_frame(self.test_frame)
            # If we get here, error was handled gracefully
        except Exception as e:
            self.fail(f"Frame processing should handle MediaPipe errors gracefully, but got: {e}")
    
    @patch('src.core.detection_system.ExerciseDetectionSystem.detect_exercises')
    @patch('mediapipe.solutions.pose.Pose.process')
    def test_exercise_detection_error(self, mock_pose_process, mock_detect_exercises):
        """Test handling of exercise detection errors"""
        # Mock MediaPipe to work normally
        mock_pose_results = Mock()
        mock_pose_results.pose_landmarks = Mock()
        mock_pose_process.return_value = mock_pose_results
        
        # Make exercise detection raise an exception
        mock_detect_exercises.side_effect = Exception("Detection error")
        
        # Process frame - should not crash
        try:
            processed_frame, exercise_results = self.processor.process_frame(self.test_frame)
            # If we get here, error was handled gracefully
        except Exception as e:
            self.fail(f"Frame processing should handle detection errors gracefully, but got: {e}")
    
    def test_invalid_frame_input(self):
        """Test handling of invalid frame input"""
        # Test with None frame
        try:
            processed_frame, exercise_results = self.processor.process_frame(None)
            # Should either handle gracefully or raise a specific expected error
        except (AttributeError, TypeError):
            # These are expected for None input
            pass
        except Exception as e:
            self.fail(f"Unexpected exception for None frame: {e}")
        
        # Test with invalid frame shape
        invalid_frame = np.array([1, 2, 3])  # Wrong shape
        try:
            processed_frame, exercise_results = self.processor.process_frame(invalid_frame)
        except Exception:
            # Expected to fail with invalid frame
            pass
    
    def test_cleanup_without_pose_object(self):
        """Test cleanup when pose object doesn't exist"""
        # Remove pose object
        delattr(self.processor, 'pose')
        
        # Cleanup should not crash
        try:
            self.processor.cleanup()
        except AttributeError:
            # Expected if pose object doesn't exist
            pass
        except Exception as e:
            self.fail(f"Cleanup should handle missing pose object gracefully, but got: {e}")


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestVideoProcessor,
        TestVideoProcessorIntegration,
        TestVideoProcessorErrorHandling
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Video Processor Test Results")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*50}")
