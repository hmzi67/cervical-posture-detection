# Project Documentation

## Cervical Pose Detection System

### Overview

A real-time computer vision system for detecting and providing feedback on cervical exercises using MediaPipe pose estimation.

### Features

- Real-time pose detection using MediaPipe
- Detection of 5 cervical exercises:
  - Cervical Flexion (Chin-to-Chest)
  - Cervical Extension (Look Upward)
  - Lateral Neck Tilt
  - Neck Rotation
  - Chin Tuck
- Automatic calibration system
- Real-time visual feedback
- Performance metrics and statistics
- Configurable detection thresholds

### Project Structure

```
cpd-2/
├── src/
│   ├── core/
│   │   ├── models.py          # Data models and enums
│   │   ├── detection_system.py # Main detection coordinator
│   │   └── video_processor.py  # Video processing and visualization
│   ├── detectors/
│   │   └── exercise_detectors.py # Individual exercise detectors
│   ├── utils/
│   │   └── geometry.py        # Geometric calculations
│   └── ui/
│       └── components.py      # Streamlit UI components
├── config/
│   └── settings.py           # Configuration constants
├── tests/                    # Unit tests (future)
├── docs/                     # Documentation
├── main.py                   # Main Streamlit application
├── requirements.txt          # Dependencies
└── README.md                # Project documentation
```

### Installation

1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `streamlit run main.py`

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
