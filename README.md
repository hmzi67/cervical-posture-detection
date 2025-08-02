# Cervical Pose Detection System 🏥

A production-ready real-time computer vision system for detecting and providing feedback on cervical exercises using MediaPipe pose estimation and Streamlit.

## 🌟 Features

- **Real-time Pose Detection**: Uses MediaPipe for accurate pose landmark detection
- **5 Cervical Exercises**: Comprehensive detection for common cervical exercises
- **Automatic Calibration**: Self-calibrating system for personalized detection
- **Visual Feedback**: Real-time overlay and status panel feedback
- **Performance Monitoring**: FPS tracking and system statistics
- **Modular Architecture**: Clean, extensible codebase
- **Professional UI**: Modern Streamlit interface with custom styling

## 🎯 Supported Exercises

1. **Cervical Flexion** - Chin-to-chest movement
2. **Cervical Extension** - Looking upward movement
3. **Lateral Neck Tilt** - Side-to-side head tilting
4. **Neck Rotation** - Left-right head turning
5. **Chin Tuck** - Backward chin movement

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Webcam or camera device
- Good lighting conditions

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd cpd-2

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run main.py
```

### Usage

1. **Setup**: Select your camera from the sidebar
2. **Configure**: Choose exercises to monitor and adjust settings
3. **Start**: Click the Start button to begin detection
4. **Calibrate**: Stay still for automatic calibration (15 frames)
5. **Exercise**: Perform exercises for real-time feedback

## 📁 Project Structure

```
cpd-2/
├── src/                          # Source code
│   ├── core/                     # Core system components
│   │   ├── models.py            # Data models and types
│   │   ├── detection_system.py  # Main detection coordinator
│   │   └── video_processor.py   # Video processing engine
│   ├── detectors/               # Exercise detection algorithms
│   │   └── exercise_detectors.py
│   ├── utils/                   # Utility functions
│   │   └── geometry.py          # Geometric calculations
│   └── ui/                      # User interface components
│       └── components.py        # Streamlit UI components
├── config/                      # Configuration files
│   └── settings.py             # System settings
├── docs/                        # Documentation
├── tests/                       # Unit tests (future)
├── main.py                      # Main application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🔧 Configuration

The system is highly configurable through `config/settings.py`:

- **Detection Thresholds**: Adjust sensitivity for each exercise
- **Calibration Settings**: Frame count and smoothing parameters
- **Performance Settings**: FPS limits and video resolution
- **UI Settings**: Display options and feedback parameters

## 🎨 Technical Architecture

### Core Components

- **Models**: Type-safe data structures using dataclasses and enums
- **Detectors**: Individual exercise detection algorithms with calibration
- **Video Processor**: Real-time video processing and visualization
- **UI Components**: Reusable Streamlit interface elements

### Key Features

- **Automatic Calibration**: Self-adjusting baselines for personalized detection
- **Confidence Smoothing**: Stable feedback through exponential smoothing
- **Error Handling**: Comprehensive error handling and user feedback
- **Performance Monitoring**: Real-time FPS and processing statistics

## 📊 Detection Algorithm

Each exercise detector follows a consistent pattern:

1. **Calibration Phase**: Collect baseline measurements (15 frames)
2. **Detection Phase**: Compare current pose to calibrated baseline
3. **Confidence Calculation**: Generate confidence scores (0-100%)
4. **Feedback Generation**: Provide real-time status messages

### Exercise-Specific Logic

- **Flexion/Extension**: Distance ratio between nose and shoulders
- **Lateral Tilt**: Asymmetry in nose-to-ear distances
- **Rotation**: Visibility changes of ears relative to nose
- **Chin Tuck**: Horizontal offset and vertical depth changes

## 🛠️ Development

### Adding New Exercises

1. Create detector class inheriting from `BaseDetector`
2. Implement required abstract methods
3. Add to `ExerciseDetectionSystem`
4. Update UI components

### Testing

```bash
# Run basic import test
python -c "from src.core.models import *; print('✅ Imports successful')"

# Test detection system
python -c "from src.core.detection_system import ExerciseDetectionSystem; print('✅ System ready')"
```

## 📋 Requirements

- `streamlit>=1.28.0` - Web application framework
- `opencv-python>=4.8.0` - Computer vision library
- `mediapipe>=0.10.0` - Pose detection framework
- `numpy>=1.24.0` - Numerical computing

## 🎯 Future Enhancements

- [ ] Exercise session recording and playback
- [ ] Progress tracking and analytics
- [ ] Mobile device support
- [ ] Multi-person detection
- [ ] Custom exercise creation
- [ ] Cloud storage integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- MediaPipe team for the pose estimation framework
- Streamlit team for the web application framework
- OpenCV community for computer vision tools

---

**Built with ❤️ for healthcare and rehabilitation professionals**
