# Cervical Pose Detection System - Technical Documentation

## Overview

The Cervical Pose Detection System is a comprehensive real-time computer vision application designed for healthcare professionals, physical therapists, and patients to monitor and provide feedback on cervical exercise performance. Built using MediaPipe pose estimation, OpenCV, and Streamlit, the system offers accurate detection of five key cervical exercises with automatic calibration and real-time feedback.

## Clinical Applications

### Target Users

- **Physical Therapists**: Monitor patient exercise compliance and form
- **Healthcare Professionals**: Assess cervical range of motion and function
- **Patients**: Receive real-time feedback during home exercise programs
- **Researchers**: Collect objective data on cervical exercise performance

### Clinical Benefits

- **Objective Assessment**: Quantitative measurement of exercise performance
- **Real-time Feedback**: Immediate correction and encouragement
- **Progress Tracking**: Session statistics and performance metrics
- **Standardization**: Consistent exercise assessment across sessions
- **Accessibility**: Home-based exercise monitoring capability

## System Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Streamlit UI   │  │   Controls      │  │  Feedback   │  │
│  │   Components     │  │   Panel         │  │   Display   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
│
┌─────────────────────────────────────────────────────────────┐
│                  Video Processing Layer                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │  Video Capture  │  │   MediaPipe     │  │ Landmark    │  │
│  │  & Processing   │  │ Pose Detection  │  │ Extraction  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
│
┌─────────────────────────────────────────────────────────────┐
│                Exercise Detection Layer                     │
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────────┐  │
│  │   Cervical    │ │   Cervical    │ │   Lateral Neck    │  │
│  │   Flexion     │ │  Extension    │ │     Tilt          │  │
│  └───────────────┘ └───────────────┘ └───────────────────┘  │
│  ┌───────────────┐ ┌───────────────┐                       │
│  │     Neck      │ │   Chin Tuck   │                       │
│  │   Rotation    │ │   Detector    │                       │
│  └───────────────┘ └───────────────┘                       │
└─────────────────────────────────────────────────────────────┘
│
┌─────────────────────────────────────────────────────────────┐
│                   Data & Analysis Layer                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Geometry      │  │   Statistical   │  │ Performance │  │
│  │   Calculations  │  │   Analysis      │  │  Monitoring │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Video Capture**: Real-time camera feed acquisition
2. **Pose Detection**: MediaPipe landmark extraction (33 key points)
3. **Landmark Processing**: Key cervical landmarks isolation and validation
4. **Exercise Analysis**: Individual detector processing with confidence scoring
5. **Result Aggregation**: Combined exercise status and feedback generation
6. **UI Updates**: Real-time display updates and user feedback

## Exercise Detection Algorithms

### Calibration Process

Each exercise detector implements a two-phase approach:

#### Phase 1: Calibration (15 frames)

1. **Baseline Collection**: Capture neutral position measurements
2. **Statistical Processing**: Calculate median values for robustness
3. **Threshold Personalization**: Adapt detection thresholds to individual anatomy
4. **Validation**: Ensure sufficient data quality before proceeding

#### Phase 2: Detection

1. **Real-time Analysis**: Compare current pose to calibrated baseline
2. **Confidence Calculation**: Generate probability scores (0-100%)
3. **Smoothing**: Apply temporal filtering to reduce noise
4. **Feedback Generation**: Create actionable user guidance

### Exercise-Specific Detection Methods

#### 1. Cervical Flexion (Chin-to-chest)

- **Measurement**: Euclidean distance from nose to midpoint of shoulders
- **Detection Logic**: Distance ratio < 0.85 (configurable)
- **Clinical Rationale**: Forward flexion reduces nose-to-shoulder distance
- **Common Issues**: Ensure shoulders remain level, avoid neck shortening

#### 2. Cervical Extension (Look upward)

- **Measurement**: Euclidean distance from nose to midpoint of shoulders
- **Detection Logic**: Distance ratio > 1.15 (configurable)
- **Clinical Rationale**: Extension increases nose-to-shoulder distance
- **Common Issues**: Avoid excessive extension, monitor for dizziness

#### 3. Lateral Neck Tilt (Left and Right)

- **Measurement**: Asymmetry in nose-to-ear distances (left vs right)
- **Detection Logic**: Absolute difference > 0.15 (configurable)
- **Clinical Rationale**: Lateral flexion creates asymmetrical ear-nose relationships
- **Common Issues**: Keep shoulders level, avoid compensation patterns

#### 4. Neck Rotation (Turn head left/right)

- **Measurement**: Relative visibility of ears based on horizontal displacement
- **Detection Logic**: Visibility ratio > 1.5 (configurable)
- **Clinical Rationale**: Rotation changes relative ear positions
- **Common Issues**: Maintain chin level, avoid tilting during rotation

#### 5. Chin Tuck (Retract chin)

- **Measurement**: Horizontal offset and vertical depth relative to ear midpoint
- **Detection Logic**: Offset ratio < 0.8 AND depth ratio > 1.05
- **Clinical Rationale**: Posterior translation reduces horizontal offset
- **Common Issues**: Avoid chin depression, maintain level head position

## Configuration Parameters

### Detection Thresholds

```python
# Default values optimized for average adult anatomy
CERVICAL_FLEXION_THRESHOLD = 0.85      # More sensitive = lower value
CERVICAL_EXTENSION_THRESHOLD = 1.15    # More sensitive = lower value
LATERAL_TILT_THRESHOLD = 0.15          # More sensitive = lower value
NECK_ROTATION_THRESHOLD = 1.5          # More sensitive = lower value
CHIN_TUCK_THRESHOLD = 0.8              # More sensitive = lower value
```

### System Performance

```python
# Calibration settings
CALIBRATION_FRAMES = 15                # Frames for baseline (1 second at 15 FPS)
CONFIDENCE_SMOOTHING = 0.3             # Temporal smoothing factor (0-1)

# MediaPipe settings
MIN_DETECTION_CONFIDENCE = 0.5         # Initial pose detection threshold
MIN_TRACKING_CONFIDENCE = 0.5          # Pose tracking threshold
MODEL_COMPLEXITY = 1                   # 0=light, 1=full, 2=heavy

# Performance settings
DEFAULT_FPS = 15                       # Target frame rate
VIDEO_WIDTH = 640                      # Camera resolution width
VIDEO_HEIGHT = 480                     # Camera resolution height
```

## Installation & Deployment

### System Requirements

- **Python**: 3.10 or higher
- **RAM**: Minimum 4GB, recommended 8GB
- **CPU**: Multi-core processor recommended
- **Camera**: USB webcam or built-in camera
- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+

### Dependencies

```bash
# Core dependencies
streamlit>=1.28.1          # Web application framework
opencv-python>=4.8.1.78    # Computer vision library
mediapipe>=0.10.7          # Google's pose estimation
numpy>=1.24.3              # Numerical computing

# Additional utilities
pandas>=2.0.3              # Data manipulation
Pillow>=10.0.1             # Image processing
matplotlib>=3.7.2          # Plotting (optional)
```

### Installation Steps

```bash
# 1. Clone repository
git clone https://github.com/your-repo/cervical-pose-detection
cd cervical-pose-detection

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
streamlit run main.py
```

## Usage Guidelines

### Clinical Setup Recommendations

#### Environment Setup

- **Lighting**: Use even, frontal lighting; avoid backlighting
- **Background**: Simple, uncluttered background; avoid busy patterns
- **Camera Position**: Position camera at eye level, 3-5 feet from patient
- **Seating**: Use stable chair with back support; avoid swivel chairs

#### Patient Preparation

- **Clothing**: Wear contrasting colors; avoid white/black or striped patterns
- **Hair**: Secure long hair to clearly expose ears and neck
- **Posture**: Maintain upright seated posture with feet flat on floor
- **Instructions**: Explain the calibration process and exercise expectations

#### Session Protocol

1. **Initial Calibration**:

   - Patient maintains neutral head position
   - System calibrates each exercise (15 frames per exercise)
   - Verify "Ready" status for all exercises before proceeding

2. **Exercise Performance**:

   - Perform exercises slowly and deliberately
   - Hold end-range positions for 2-3 seconds
   - Follow real-time feedback guidance
   - Complete 3-5 repetitions per exercise direction

3. **Session Monitoring**:
   - Monitor confidence scores (target >70%)
   - Watch for error messages or detection failures
   - Reset calibration if accuracy decreases
   - Document session statistics for progress tracking

### Troubleshooting Guide

#### Common Issues and Solutions

**Poor Detection Accuracy**

- Check lighting conditions and camera angle
- Ensure clear visibility of head, shoulders, and ears
- Reset calibration if environmental conditions changed
- Verify camera is not moving during session

**Calibration Failures**

- Ensure patient maintains completely still neutral position
- Check for adequate lighting on face and shoulders
- Verify all required landmarks are visible
- Restart system if persistent issues occur

**Performance Issues**

- Reduce FPS limit in sidebar settings
- Close other applications using camera
- Check system resources (CPU, memory usage)
- Update graphics drivers if using integrated graphics

**False Positives/Negatives**

- Adjust detection thresholds in advanced settings
- Re-calibrate with better neutral positioning
- Check for movement artifacts or camera shake
- Verify exercise technique matches clinical standards

## Technical Implementation Details

### MediaPipe Integration

The system uses Google's MediaPipe Pose solution for real-time pose detection:

```python
# MediaPipe initialization
self.mp_pose = mp.solutions.pose
self.pose = self.mp_pose.Pose(
    static_image_mode=False,           # Video stream mode
    model_complexity=1,                # Balance accuracy/performance
    enable_segmentation=False,         # Disable background removal
    min_detection_confidence=0.5,      # Detection threshold
    min_tracking_confidence=0.5        # Tracking threshold
)
```

### Key Landmarks Used

From MediaPipe's 33-point pose model, the system primarily uses:

- **Landmark 0**: Nose tip
- **Landmark 7**: Left ear
- **Landmark 8**: Right ear
- **Landmark 11**: Left shoulder
- **Landmark 12**: Right shoulder

### Mathematical Foundations

#### Distance Calculations

```python
def calculate_distance(point1: np.ndarray, point2: np.ndarray) -> float:
    """Euclidean distance between two 2D points"""
    return np.linalg.norm(point1 - point2)
```

#### Ratio Analysis

```python
def calculate_ratio(distance: float, baseline: float) -> float:
    """Ratio calculation with zero-baseline protection"""
    return distance / baseline if baseline != 0 else 1.0
```

#### Confidence Smoothing

```python
def smooth_value(current: float, previous: float, factor: float = 0.3) -> float:
    """Exponential smoothing for temporal consistency"""
    return factor * current + (1 - factor) * previous
```

## Quality Assurance

### Testing Framework

The system includes comprehensive unit tests covering:

- **Data Models**: Validation of core data structures
- **Geometry Utilities**: Mathematical function accuracy
- **Detection System**: Exercise-specific algorithm testing
- **Video Processing**: MediaPipe integration and frame handling
- **Error Handling**: Graceful degradation and recovery

### Performance Metrics

- **Frame Rate**: Target 15 FPS, acceptable range 10-30 FPS
- **Detection Latency**: <100ms per frame processing
- **Calibration Time**: ~1 second (15 frames at 15 FPS)
- **Memory Usage**: <500MB typical operation
- **CPU Usage**: <50% on modern multi-core systems

### Validation Studies

The system has been tested with:

- Various lighting conditions (indoor/outdoor/artificial)
- Different camera angles and distances
- Multiple user demographics (age, size, mobility)
- Clinical exercise protocols and standards

## Future Enhancements

### Planned Features

- **Cloud Storage**: Session data backup and synchronization
- **Advanced Analytics**: Trend analysis and progress reports
- **Multi-user Support**: Patient profiles and history tracking
- **Integration APIs**: EMR/EHR system connectivity
- **Mobile App**: iOS/Android companion applications

### Research Opportunities

- **Machine Learning**: Personalized threshold adaptation
- **Computer Vision**: Enhanced landmark detection accuracy
- **Clinical Studies**: Validation against gold-standard goniometry
- **Accessibility**: Voice commands and alternative input methods

## Support and Maintenance

### Documentation Updates

- System documentation is maintained with each software release
- Clinical protocols updated based on user feedback
- Performance benchmarks updated with each major version

### Issue Reporting

- Technical issues: GitHub Issues tracker
- Clinical questions: Clinical support documentation
- Feature requests: Product roadmap discussions

### Version Control

- Semantic versioning (MAJOR.MINOR.PATCH)
- Backwards compatibility maintained for configuration files
- Migration guides provided for breaking changes

---

**Last Updated**: August 2025  
**Document Version**: 2.0  
**System Version**: 2.2

### Usage

1. Select camera and exercises from sidebar
2. Click Start to begin detection
3. Follow calibration instructions
4. Perform exercises for real-time feedback

### Technical Details

- Uses MediaPipe for pose landmark detection
- Custom geometric algorithms for exercise recognition
- Confidence smoothing for stable feedback
- Modular architecture for easy extension
