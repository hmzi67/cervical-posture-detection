# Testing Requirements for Cervical Pose Detection System

## Overview

This document outlines the comprehensive testing requirements for the Cervical Pose Detection System. The testing framework ensures system reliability, accuracy, and clinical safety through systematic validation of all components.

## Test Categories

### 1. Unit Tests

Individual component testing for core functionality.

### 2. Integration Tests

Component interaction and data flow validation.

### 3. System Tests

End-to-end workflow and user interface testing.

### 4. Performance Tests

Speed, memory usage, and scalability validation.

### 5. Clinical Validation Tests

Accuracy and clinical utility verification.

## Test Requirements

### Prerequisites

```bash
# Install testing dependencies
pip install pytest pytest-cov pytest-mock
pip install unittest-xml-reporting

# Install the main application dependencies
pip install -r requirements.txt
```

### Running Tests

#### Complete Test Suite

```bash
# Run all tests with coverage report
python -m pytest tests/ --cov=src --cov-report=html

# Run with verbose output
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_detection_system.py -v
```

#### Quick Test Suite

```bash
# Run critical tests only
python tests/test_runner.py --quick
```

#### Performance Tests

```bash
# Run performance-focused tests
python tests/test_runner.py --performance
```

## Test Coverage Requirements

### Minimum Coverage Targets

- **Overall Code Coverage**: >85%
- **Core Detection Logic**: >95%
- **Video Processing**: >80%
- **Utility Functions**: >90%
- **Data Models**: >95%

### Critical Path Coverage

- All exercise detection algorithms: 100%
- Calibration processes: 100%
- Error handling paths: >90%
- Configuration management: 100%

## Unit Test Specifications

### Detection System Tests (`test_detection_system.py`)

#### Test Classes

1. **TestLandmarkPoints**

   - Landmark creation and validation
   - Coordinate system consistency
   - Data type verification

2. **TestCervicalFlexionDetector**

   - Calibration process validation
   - Positive detection scenarios
   - Negative detection scenarios
   - Threshold behavior testing
   - Reset functionality

3. **TestCervicalExtensionDetector**

   - Extension-specific detection logic
   - Boundary condition testing
   - Confidence scoring validation

4. **TestLateralNeckTiltDetector**

   - Asymmetry detection algorithms
   - Left/right symmetry validation
   - Direction determination accuracy

5. **TestNeckRotationDetector**

   - Rotation angle calculations
   - Visibility-based detection
   - Multi-directional testing

6. **TestChinTuckDetector**

   - Retraction movement detection
   - Horizontal/vertical offset analysis
   - Complex movement pattern validation

7. **TestExerciseDetectionSystem**
   - System-wide coordination
   - Multi-exercise processing
   - Performance statistics
   - Error propagation handling

#### Key Test Scenarios

```python
def test_detector_calibration_cycle():
    """Test complete calibration process"""
    detector = CervicalFlexionDetector()

    # Process calibration frames
    for i in range(15):
        result = detector.detect(test_landmarks)
        assert result.status == DetectionStatus.CALIBRATING

    # Verify calibration completion
    assert detector.is_calibrated
    assert detector.baseline_distance is not None

def test_exercise_detection_accuracy():
    """Test detection accuracy with known movements"""
    # Setup calibrated detector
    detector = setup_calibrated_detector()

    # Test positive detection
    flexion_landmarks = create_flexion_landmarks()
    result = detector.detect(flexion_landmarks)

    assert result.detected == True
    assert result.confidence > 0.7
    assert result.status == DetectionStatus.DETECTED

def test_error_handling():
    """Test graceful error handling"""
    detector = CervicalFlexionDetector()

    # Test with None landmarks
    result = detector.detect(None)
    assert result.status == DetectionStatus.ERROR
    assert "No pose detected" in result.status_message
```

### Geometry Utils Tests (`test_geometry_utils.py`)

#### Mathematical Function Validation

```python
def test_distance_calculation_accuracy():
    """Test Euclidean distance calculation"""
    p1 = np.array([0, 0])
    p2 = np.array([3, 4])

    distance = GeometryUtils.calculate_distance(p1, p2)
    assert abs(distance - 5.0) < 0.001

def test_angle_calculation_precision():
    """Test angle calculation for known configurations"""
    # Right angle test
    p1 = np.array([1, 0])
    p2 = np.array([0, 0])  # vertex
    p3 = np.array([0, 1])

    angle = GeometryUtils.calculate_angle(p1, p2, p3)
    assert abs(angle - 90.0) < 0.1

def test_landmark_extraction_robustness():
    """Test landmark extraction with various input conditions"""
    # Test with valid MediaPipe results
    valid_results = create_mock_pose_results()
    landmarks = LandmarkExtractor.extract_landmarks(valid_results, (480, 640, 3))
    assert landmarks is not None

    # Test with missing landmarks
    invalid_results = create_incomplete_pose_results()
    landmarks = LandmarkExtractor.extract_landmarks(invalid_results, (480, 640, 3))
    assert landmarks is None
```

### Data Models Tests (`test_models.py`)

#### Data Integrity Validation

```python
def test_exercise_result_serialization():
    """Test result serialization and deserialization"""
    result = ExerciseResult(
        exercise_type=ExerciseType.CERVICAL_FLEXION,
        detected=True,
        confidence=0.85,
        status=DetectionStatus.DETECTED,
        metrics={'ratio': 0.7}
    )

    # Test serialization
    result_dict = result.to_dict()
    assert result_dict['exercise_type'] == ExerciseType.CERVICAL_FLEXION.value
    assert result_dict['detected'] == True
    assert result_dict['confidence'] == 0.85

def test_system_config_validation():
    """Test configuration parameter validation"""
    config = SystemConfig(
        flexion_threshold=0.9,
        calibration_frames=20
    )

    assert config.flexion_threshold == 0.9
    assert config.calibration_frames == 20

    # Test default values
    assert config.extension_threshold == 1.15  # default value
```

### Video Processor Tests (`test_video_processor.py`)

#### MediaPipe Integration Testing

```python
@patch('mediapipe.solutions.pose.Pose.process')
def test_frame_processing_pipeline(mock_pose_process):
    """Test complete frame processing pipeline"""
    # Mock MediaPipe response
    mock_pose_results = Mock()
    mock_pose_results.pose_landmarks = Mock()
    mock_pose_process.return_value = mock_pose_results

    processor = VideoProcessor()
    test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

    # Process frame
    processed_frame, results = processor.process_frame(test_frame)

    # Validate outputs
    assert processed_frame.shape == test_frame.shape
    assert isinstance(results, dict)
    assert len(results) == 5  # All 5 exercises

def test_performance_monitoring():
    """Test performance tracking functionality"""
    processor = VideoProcessor()

    # Process multiple frames
    for _ in range(10):
        processor.process_frame(test_frame)

    stats = processor.get_system_stats()

    assert stats['frame_count'] == 10
    assert stats['avg_fps'] > 0
    assert len(processor.processing_times) == 10
```

## Integration Test Specifications

### System Integration Tests

#### End-to-End Workflow Testing

```python
def test_complete_detection_workflow():
    """Test complete system workflow from camera to results"""
    # Initialize system components
    config = SystemConfig()
    video_processor = VideoProcessor(config)

    # Simulate camera frames
    test_frames = generate_test_frame_sequence()

    results_history = []
    for frame in test_frames:
        processed_frame, exercise_results = video_processor.process_frame(frame)
        results_history.append(exercise_results)

    # Validate progression through calibration to detection
    assert results_history[0][ExerciseType.CERVICAL_FLEXION].status == DetectionStatus.CALIBRATING
    assert results_history[-1][ExerciseType.CERVICAL_FLEXION].status in [DetectionStatus.READY, DetectionStatus.DETECTED]

def test_multi_exercise_coordination():
    """Test coordination between multiple exercise detectors"""
    system = ExerciseDetectionSystem()

    # Test with landmarks showing multiple exercises
    multi_exercise_landmarks = create_complex_movement_landmarks()
    results = system.detect_exercises(mock_pose_results, (480, 640, 3))

    # Verify independent detection
    flexion_detected = results[ExerciseType.CERVICAL_FLEXION].detected
    rotation_detected = results[ExerciseType.NECK_ROTATION].detected

    # Should be able to detect multiple exercises simultaneously
    assert len([r for r in results.values() if r.detected]) <= 2
```

## Performance Test Specifications

### Real-time Performance Requirements

#### Frame Processing Speed

```python
def test_real_time_processing_speed():
    """Test system maintains real-time performance"""
    processor = VideoProcessor()
    test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

    start_time = time.time()
    frame_count = 30  # 2 seconds at 15 FPS

    for _ in range(frame_count):
        processor.process_frame(test_frame)

    total_time = time.time() - start_time
    fps = frame_count / total_time

    # Should maintain at least 10 FPS for real-time performance
    assert fps >= 10.0

def test_memory_usage_stability():
    """Test memory usage remains stable over time"""
    import psutil
    import os

    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss

    processor = VideoProcessor()

    # Process many frames
    for _ in range(1000):
        processor.process_frame(test_frame)

    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory

    # Memory increase should be minimal (less than 100MB)
    assert memory_increase < 100 * 1024 * 1024
```

#### Calibration Performance

```python
def test_calibration_speed():
    """Test calibration completes within acceptable time"""
    detector = CervicalFlexionDetector()

    start_time = time.time()

    # Complete calibration process
    for _ in range(15):
        detector.detect(test_landmarks)

    calibration_time = time.time() - start_time

    # Calibration should complete in under 2 seconds
    assert calibration_time < 2.0
    assert detector.is_calibrated
```

## Clinical Validation Test Specifications

### Accuracy Validation

#### Ground Truth Testing

```python
def test_detection_accuracy_against_ground_truth():
    """Test detection accuracy against known movements"""
    # Test with pre-recorded sessions with known exercise performance
    test_sessions = load_ground_truth_sessions()

    for session in test_sessions:
        processor = VideoProcessor()

        total_predictions = 0
        correct_predictions = 0

        for frame, expected_results in session:
            _, actual_results = processor.process_frame(frame)

            for exercise_type, expected in expected_results.items():
                actual = actual_results[exercise_type]

                if actual.detected == expected.detected:
                    correct_predictions += 1
                total_predictions += 1

        accuracy = correct_predictions / total_predictions
        assert accuracy > 0.85  # Minimum 85% accuracy required

def test_consistency_across_subjects():
    """Test system consistency across different users"""
    test_subjects = load_diverse_subject_data()

    for subject_data in test_subjects:
        processor = VideoProcessor()

        # Calibrate for this subject
        calibration_frames = subject_data['calibration']
        for frame in calibration_frames:
            processor.process_frame(frame)

        # Test exercise detection
        exercise_frames = subject_data['exercises']
        results = []

        for frame in exercise_frames:
            _, exercise_results = processor.process_frame(frame)
            results.append(exercise_results)

        # Verify reasonable detection rates
        detection_rates = calculate_detection_rates(results)
        assert all(rate > 0.7 for rate in detection_rates.values())
```

### Clinical Utility Testing

#### Inter-rater Reliability

```python
def test_inter_rater_reliability():
    """Test system consistency compared to human raters"""
    # Test sessions rated by multiple clinical experts
    expert_ratings = load_expert_ratings()

    for session_id, ratings in expert_ratings.items():
        system_results = run_system_on_session(session_id)

        # Compare system detection to expert consensus
        agreement_scores = []

        for exercise_type in ExerciseType:
            expert_consensus = calculate_expert_consensus(ratings, exercise_type)
            system_detection = system_results[exercise_type].detected

            agreement = 1.0 if system_detection == expert_consensus else 0.0
            agreement_scores.append(agreement)

        overall_agreement = np.mean(agreement_scores)
        assert overall_agreement > 0.8  # 80% agreement with experts
```

## Automated Test Execution

### Continuous Integration Setup

#### GitHub Actions Configuration

```yaml
name: Cervical Pose Detection Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run unit tests
        run: pytest tests/ --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v1
```

#### Pre-commit Hooks

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Manual run
pre-commit run --all-files
```

### Test Data Management

#### Test Asset Organization

```
tests/
├── data/
│   ├── ground_truth/          # Validated test sessions
│   ├── synthetic/             # Generated test data
│   ├── edge_cases/            # Boundary condition tests
│   └── performance/           # Performance benchmarking data
├── fixtures/                  # Reusable test fixtures
├── mocks/                     # Mock objects and responses
└── utils/                     # Testing utility functions
```

#### Test Data Requirements

- **Ground Truth Sessions**: 50+ validated exercise sessions
- **Synthetic Data**: Programmatically generated landmarks
- **Edge Cases**: Boundary conditions and error scenarios
- **Performance Data**: Large datasets for stress testing

## Test Reporting

### Coverage Reports

```bash
# Generate HTML coverage report
pytest tests/ --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Performance Benchmarking

```bash
# Run performance tests with timing
pytest tests/test_performance.py --benchmark-only

# Generate performance report
python tests/benchmark_runner.py --output=performance_report.html
```

### Clinical Validation Reports

```bash
# Run clinical validation suite
python tests/clinical_validation.py --report=clinical_validation_report.pdf
```

## Test Maintenance

### Regular Test Updates

- **Weekly**: Update test data with new clinical scenarios
- **Monthly**: Review and update performance benchmarks
- **Quarterly**: Comprehensive test suite review
- **Annually**: Clinical validation study updates

### Test Quality Metrics

- **Test Coverage**: Monitor and maintain >85% coverage
- **Test Execution Time**: Keep full suite under 5 minutes
- **Test Reliability**: <1% flaky test rate
- **Documentation**: 100% test documentation coverage

---

**Testing Framework Version**: 1.0  
**Last Updated**: August 2025  
**Test Lead**: [Name]  
**Clinical Validation Lead**: [Name]
