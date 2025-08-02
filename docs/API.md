# API Documentation - Cervical Pose Detection System

## Core Classes and Methods

### ExerciseDetectionSystem

Main coordinator class for all exercise detection functionality.

#### Constructor

```python
ExerciseDetectionSystem(config: SystemConfig = None)
```

**Parameters:**

- `config` (SystemConfig, optional): Configuration object with detection thresholds and system settings

**Example:**

```python
from src.core.detection_system import ExerciseDetectionSystem
from src.core.models import SystemConfig

config = SystemConfig(
    flexion_threshold=0.85,
    calibration_frames=15
)
system = ExerciseDetectionSystem(config)
```

#### Methods

##### detect_exercises()

```python
detect_exercises(pose_results, frame_shape) -> Dict[ExerciseType, ExerciseResult]
```

**Description:** Detects all exercises from MediaPipe pose results.

**Parameters:**

- `pose_results`: MediaPipe pose detection results
- `frame_shape` (tuple): Frame dimensions (height, width, channels)

**Returns:**

- Dictionary mapping ExerciseType to ExerciseResult objects

**Example:**

```python
results = system.detect_exercises(pose_results, (480, 640, 3))
for exercise_type, result in results.items():
    print(f"{exercise_type.value}: {result.detected} ({result.confidence:.2f})")
```

##### reset_baselines()

```python
reset_baselines() -> None
```

**Description:** Resets calibration for all exercise detectors.

**Example:**

```python
system.reset_baselines()  # Recalibrate all exercises
```

##### get_system_stats()

```python
get_system_stats() -> dict
```

**Description:** Returns system performance statistics.

**Returns:**

- Dictionary with keys: `total_detections`, `session_duration`, `detections_per_second`, `active_detectors`

---

### VideoProcessor

Handles video processing and MediaPipe integration.

#### Constructor

```python
VideoProcessor(config: SystemConfig = None)
```

**Parameters:**

- `config` (SystemConfig, optional): Configuration for video processing

#### Methods

##### process_frame()

```python
process_frame(frame: np.ndarray) -> Tuple[np.ndarray, Dict[ExerciseType, ExerciseResult]]
```

**Description:** Processes a single video frame.

**Parameters:**

- `frame` (np.ndarray): Input frame in BGR format

**Returns:**

- Tuple of (processed_frame, exercise_results)

**Example:**

```python
import cv2
from src.core.video_processor import VideoProcessor

processor = VideoProcessor()
cap = cv2.VideoCapture(0)

ret, frame = cap.read()
if ret:
    processed_frame, results = processor.process_frame(frame)
    cv2.imshow('Processed', processed_frame)
```

##### get_system_stats()

```python
get_system_stats() -> dict
```

**Description:** Returns video processing performance statistics.

**Returns:**

- Dictionary with keys: `frame_count`, `avg_fps`, `avg_processing_time`, `detectors_count`

---

### GeometryUtils

Static utility class for geometric calculations.

#### Methods

##### calculate_distance()

```python
@staticmethod
calculate_distance(point1: np.ndarray, point2: np.ndarray) -> float
```

**Description:** Calculates Euclidean distance between two points.

**Parameters:**

- `point1` (np.ndarray): First point [x, y]
- `point2` (np.ndarray): Second point [x, y]

**Returns:**

- Float distance value

**Example:**

```python
from src.utils.geometry import GeometryUtils
import numpy as np

p1 = np.array([0, 0])
p2 = np.array([3, 4])
distance = GeometryUtils.calculate_distance(p1, p2)  # Returns 5.0
```

##### calculate_angle()

```python
@staticmethod
calculate_angle(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> float
```

**Description:** Calculates angle formed by three points (p1-p2-p3).

**Parameters:**

- `p1` (np.ndarray): First point
- `p2` (np.ndarray): Vertex point
- `p3` (np.ndarray): Third point

**Returns:**

- Angle in degrees (0-180)

##### calculate_ratio()

```python
@staticmethod
calculate_ratio(distance: float, baseline: float) -> float
```

**Description:** Calculates ratio with baseline, handling edge cases.

**Parameters:**

- `distance` (float): Current distance
- `baseline` (float): Reference baseline distance

**Returns:**

- Ratio value (handles division by zero)

##### smooth_value()

```python
@staticmethod
smooth_value(current: float, previous: float, smoothing_factor: float = 0.3) -> float
```

**Description:** Applies exponential smoothing to reduce noise.

**Parameters:**

- `current` (float): Current value
- `previous` (float): Previous smoothed value
- `smoothing_factor` (float): Smoothing strength (0-1)

**Returns:**

- Smoothed value

---

### LandmarkExtractor

Handles extraction of key pose landmarks from MediaPipe results.

#### Methods

##### extract_landmarks()

```python
@staticmethod
extract_landmarks(pose_results, frame_shape) -> Optional[LandmarkPoints]
```

**Description:** Extracts key cervical landmarks from pose results.

**Parameters:**

- `pose_results`: MediaPipe pose detection results
- `frame_shape` (tuple): Frame dimensions for coordinate conversion

**Returns:**

- LandmarkPoints object or None if extraction fails

**Example:**

```python
from src.utils.geometry import LandmarkExtractor

landmarks = LandmarkExtractor.extract_landmarks(pose_results, (480, 640, 3))
if landmarks:
    print(f"Nose position: {landmarks.nose}")
    print(f"Left ear: {landmarks.left_ear}")
```

##### is_pose_visible()

```python
@staticmethod
is_pose_visible(landmarks: LandmarkPoints, min_visibility: float = 0.5) -> bool
```

**Description:** Validates pose landmark visibility and quality.

**Parameters:**

- `landmarks` (LandmarkPoints): Extracted landmark points
- `min_visibility` (float): Minimum visibility threshold

**Returns:**

- Boolean indicating if pose is sufficiently visible

---

## Data Models

### ExerciseType (Enum)

Enumeration of supported cervical exercises.

**Values:**

- `CERVICAL_FLEXION`: "Cervical Flexion (Chin-to-chest)"
- `CERVICAL_EXTENSION`: "Cervical Extension (Look upward)"
- `LATERAL_NECK_TILT`: "Lateral Neck Tilt (Left and Right)"
- `NECK_ROTATION`: "Neck Rotation (Turn head left/right)"
- `CHIN_TUCK`: "Chin Tuck (Retract chin)"

### DetectionStatus (Enum)

Status of exercise detection process.

**Values:**

- `CALIBRATING`: "calibrating"
- `READY`: "ready"
- `DETECTED`: "detected"
- `NOT_DETECTED`: "not_detected"
- `ERROR`: "error"

### LandmarkPoints (DataClass)

Container for key cervical pose landmarks.

**Attributes:**

- `nose` (np.ndarray): Nose tip coordinates [x, y]
- `left_ear` (np.ndarray): Left ear coordinates [x, y]
- `right_ear` (np.ndarray): Right ear coordinates [x, y]
- `left_shoulder` (np.ndarray): Left shoulder coordinates [x, y]
- `right_shoulder` (np.ndarray): Right shoulder coordinates [x, y]

### ExerciseResult (DataClass)

Contains detection results for a specific exercise.

**Attributes:**

- `exercise_type` (ExerciseType): Type of exercise
- `detected` (bool): Whether exercise was detected
- `confidence` (float): Confidence score (0.0-1.0)
- `status` (DetectionStatus): Current detection status
- `status_message` (str): Human-readable status message
- `metrics` (dict, optional): Additional measurement data
- `timestamp` (float, optional): Result timestamp

**Methods:**

```python
to_dict() -> dict  # Convert to dictionary for serialization
```

### SystemConfig (DataClass)

System configuration parameters.

**Attributes:**

```python
# Detection thresholds
flexion_threshold: float = 0.85
extension_threshold: float = 1.15
tilt_threshold: float = 0.15
rotation_threshold: float = 1.5
chin_tuck_threshold: float = 0.8

# Calibration settings
calibration_frames: int = 15
confidence_smoothing: float = 0.3

# Performance settings
min_detection_confidence: float = 0.5
min_tracking_confidence: float = 0.5
model_complexity: int = 1

# UI settings
fps_limit: int = 15
video_width: int = 640
video_height: int = 480
```

---

## UI Components

### UIComponents

Static class containing reusable Streamlit interface elements.

#### Methods

##### render_header()

```python
@staticmethod
render_header() -> None
```

**Description:** Renders the main application header.

##### render_exercise_status_panel()

```python
@staticmethod
render_exercise_status_panel(
    exercise_results: Dict[ExerciseType, ExerciseResult],
    selected_exercise: ExerciseType = None
) -> None
```

**Description:** Renders exercise status and feedback panel.

##### render_sidebar_controls()

```python
@staticmethod
render_sidebar_controls(config: SystemConfig) -> dict
```

**Description:** Renders sidebar controls and returns user selections.

**Returns:**

- Dictionary with control values and button states

##### render_system_stats()

```python
@staticmethod
render_system_stats(stats: dict) -> None
```

**Description:** Renders system performance statistics.

### SessionManager

Manages Streamlit session state.

#### Methods

##### initialize_session_state()

```python
@staticmethod
initialize_session_state() -> None
```

**Description:** Initializes all required session state variables.

##### update_config_from_controls()

```python
@staticmethod
update_config_from_controls(controls: dict) -> None
```

**Description:** Updates system configuration from UI controls.

---

## Usage Examples

### Basic Exercise Detection

```python
import cv2
from src.core.video_processor import VideoProcessor
from src.core.models import SystemConfig, ExerciseType

# Initialize with custom configuration
config = SystemConfig(
    flexion_threshold=0.8,
    fps_limit=20
)

processor = VideoProcessor(config)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Process frame
    processed_frame, results = processor.process_frame(frame)

    # Check for cervical flexion
    flexion_result = results[ExerciseType.CERVICAL_FLEXION]
    if flexion_result.detected:
        print(f"Flexion detected! Confidence: {flexion_result.confidence:.2f}")

    # Display processed frame
    cv2.imshow('Cervical Exercise Detection', processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
processor.cleanup()
```

### Custom Exercise Detector

```python
from src.core.detection_system import BaseDetector
from src.core.models import ExerciseType, ExerciseResult, DetectionStatus

class CustomExerciseDetector(BaseDetector):
    """Custom exercise detector implementation"""

    def __init__(self, config=None):
        super().__init__(ExerciseType.CERVICAL_FLEXION, config)
        self.custom_threshold = 0.9

    def _collect_baseline_data(self, landmarks):
        # Implement custom baseline collection
        pass

    def _finalize_calibration(self):
        # Implement custom calibration finalization
        pass

    def _detect_exercise(self, landmarks):
        # Implement custom detection logic
        detected = True  # Your detection logic here
        confidence = 0.85
        metrics = {'custom_metric': 1.0}
        return detected, confidence, metrics

    def _generate_status_message(self, detected, confidence, metrics):
        if detected:
            return f"Custom exercise detected! ({confidence:.2f})"
        return "Perform custom exercise"
```

### Performance Monitoring

```python
from src.core.video_processor import VideoProcessor
import time

processor = VideoProcessor()

# Monitor performance over time
start_time = time.time()
frame_count = 0

while frame_count < 100:  # Process 100 frames
    # ... process frame ...
    frame_count += 1

    if frame_count % 30 == 0:  # Every 30 frames
        stats = processor.get_system_stats()
        print(f"Average FPS: {stats['avg_fps']:.2f}")
        print(f"Processing time: {stats['avg_processing_time']:.3f}s")

total_time = time.time() - start_time
print(f"Total processing time: {total_time:.2f}s")
print(f"Overall FPS: {frame_count / total_time:.2f}")
```

---

## Error Handling

### Common Exception Types

- `AttributeError`: Missing landmarks or pose data
- `ValueError`: Invalid configuration parameters
- `IndexError`: Insufficient landmark points
- `RuntimeError`: MediaPipe initialization failures

### Error Handling Patterns

```python
from src.core.video_processor import VideoProcessor

processor = VideoProcessor()

try:
    processed_frame, results = processor.process_frame(frame)
except AttributeError as e:
    print(f"Pose detection error: {e}")
    # Handle missing pose data
except Exception as e:
    print(f"Unexpected error: {e}")
    # Handle general errors
finally:
    processor.cleanup()  # Always cleanup resources
```

---

## Performance Optimization

### Recommended Settings

```python
# For real-time performance
config = SystemConfig(
    fps_limit=15,                    # Balance accuracy and performance
    model_complexity=1,              # Use standard MediaPipe model
    min_detection_confidence=0.5,    # Standard confidence threshold
    calibration_frames=15            # Quick calibration
)

# For maximum accuracy
config = SystemConfig(
    fps_limit=10,                    # Lower FPS for better processing
    model_complexity=2,              # Use heavy MediaPipe model
    min_detection_confidence=0.7,    # Higher confidence threshold
    calibration_frames=25            # More calibration data
)
```

### Memory Management

```python
# Proper cleanup pattern
processor = VideoProcessor()
try:
    # ... processing ...
finally:
    processor.cleanup()  # Release MediaPipe resources

# For long-running applications
if frame_count % 1000 == 0:
    # Periodic cleanup/reset
    processor.cleanup()
    processor = VideoProcessor(config)
```
