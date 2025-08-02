"""
Complete Cervical Posture Detection App with All Features
"""
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

import streamlit as st
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

# Import our enhanced modules
from src.exercise_analyzer import CervicalExerciseAnalyzer
from src.progress_tracker import ExerciseProgressTracker
from src.exercise_prescription import ExercisePrescription
from src.camera_handler import FixedCameraHandler
from src.pose_detector import CervicalPoseDetector

try:
    from src.audio_feedback import AudioFeedbackSystem
    AUDIO_AVAILABLE = True
except:
    AUDIO_AVAILABLE = False

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    st.error("⚠️ MediaPipe not available. Some features may be limited.")

# Only initialize pose detector if mediapipe is available
if MEDIAPIPE_AVAILABLE:
    from src.pose_detector import CervicalPoseDetector

# Set page config
st.set_page_config(
    page_title="Cervical Posture Detection App",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'progress_tracker' not in st.session_state:
    st.session_state.progress_tracker = ExerciseProgressTracker()
if 'prescription_system' not in st.session_state:
    st.session_state.prescription_system = ExercisePrescription()
if 'audio_system' not in st.session_state and AUDIO_AVAILABLE:
    st.session_state.audio_system = AudioFeedbackSystem()
if 'camera_handler' not in st.session_state:
    st.session_state.camera_handler = FixedCameraHandler()
if 'pose_detector' not in st.session_state and MEDIAPIPE_AVAILABLE:
    st.session_state.pose_detector = CervicalPoseDetector()
if 'exercise_analyzer' not in st.session_state:
    st.session_state.exercise_analyzer = CervicalExerciseAnalyzer()
if 'camera_started' not in st.session_state:
    st.session_state.camera_started = False
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

def add_analysis_overlay(frame, analysis_result):
    """Add exercise analysis overlay to frame"""
    h, w = frame.shape[:2]
    
    # Add status text overlay
    status_text = f"Status: {analysis_result['status']}"
    feedback_text = analysis_result['feedback']
    
    # Choose color based on status
    if analysis_result['status'] == 'Good':
        color = (0, 255, 0)  # Green
    elif analysis_result['status'] in ['Too little', 'Too much']:
        color = (0, 255, 255)  # Yellow
    else:
        color = (0, 0, 255)  # Red
    
    # Add text to frame
    cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.putText(frame, feedback_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    
    # Add angle or distance information
    if 'angle' in analysis_result:
        angle_text = f"Angle: {analysis_result['angle']:.1f}°"
        cv2.putText(frame, angle_text, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    elif 'distance' in analysis_result:
        distance_text = f"Distance: {analysis_result['distance']:.3f}"
        cv2.putText(frame, distance_text, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

def main():
    st.title("🏥 Advanced Cervical Posture Detection App")
    st.markdown("### Complete physiotherapy solution with progress tracking and personalized routines")
    
    # Sidebar with enhanced options
    st.sidebar.title("🎯 Exercise Management")
    
    # Exercise selection
    exercise_options = [
        "Cervical Flexion (Chin-to-chest)",
        "Cervical Extension (Look upward)",
        "Lateral Neck Tilt (Left and Right)",
        "Neck Rotation (Turn head left/right)",
        "Chin Tuck (Retract chin)"
    ]
    
    selected_exercise = st.sidebar.selectbox("Choose an exercise:", exercise_options)
    
    # Exercise prescription
    st.sidebar.subheader("📋 Exercise Prescription")
    fitness_level = st.sidebar.selectbox("Fitness Level:", ["beginner", "intermediate"])
    
    if st.sidebar.button("📅 View Weekly Schedule"):
        prescription = st.session_state.prescription_system.get_prescription(fitness_level)
        schedule = st.session_state.prescription_system.create_weekly_schedule(prescription)
        
        st.sidebar.markdown("**This Week's Schedule:**")
        for day, exercises in schedule.items():
            if exercises:
                st.sidebar.markdown(f"**{day}:**")
                for ex in exercises:
                    st.sidebar.markdown(f"- {ex['exercise']}: {ex['sets']}x{ex['reps']}")
    
    # Audio settings
    if AUDIO_AVAILABLE:
        st.sidebar.subheader("🔊 Audio Feedback")
        audio_enabled = st.sidebar.checkbox("Enable voice guidance", value=True)
        if hasattr(st.session_state, 'audio_system'):
            if audio_enabled:
                st.session_state.audio_system.enable_audio()
            else:
                st.session_state.audio_system.disable_audio()
    
    # Camera debug information
    st.sidebar.subheader("📹 Camera Status")
    if st.session_state.camera_started:
        st.sidebar.success("✅ Camera Active")
        camera_info = st.session_state.camera_handler.get_camera_info()
        if camera_info:
            st.sidebar.text(f"Resolution: {camera_info.get('width', 'N/A')}x{camera_info.get('height', 'N/A')}")
            st.sidebar.text(f"Index: {camera_info.get('index', 'N/A')}")
    else:
        st.sidebar.warning("⚠️ Camera Not Started")
    
    # Camera test button
    if st.sidebar.button("🔍 Test Camera"):
        available_cameras = st.session_state.camera_handler.find_available_cameras()
        if available_cameras:
            st.sidebar.success(f"Found {len(available_cameras)} camera(s)")
            for i, (idx, backend) in enumerate(available_cameras):
                st.sidebar.text(f"Camera {i+1}: Index {idx}, Backend {backend}")
        else:
            st.sidebar.error("No cameras detected")
    
    # Performance settings
    st.sidebar.subheader("⚙️ Performance")
    fps_target = st.sidebar.slider("FPS Target", 5, 30, 15)
    confidence_threshold = st.sidebar.slider("Detection Confidence", 0.5, 1.0, 0.7)
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["🎥 Live Exercise", "📊 Progress Tracking", "📋 Exercise Plans"])
    
    with tab1:
        # Live exercise interface (existing code enhanced)
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📹 Live Camera Feed")
            
            # Controls with timer
            col1_1, col1_2, col1_3 = st.columns([1, 1, 1])
            with col1_1:
                if st.button("▶️ Start Exercise", type="primary"):
                    st.session_state.is_running = True
                    st.session_state.progress_tracker.start_exercise(selected_exercise)
                    
                    # Initialize camera if not already started
                    if not st.session_state.camera_started:
                        with st.spinner("Starting camera..."):
                            # Find available cameras
                            available_cameras = st.session_state.camera_handler.find_available_cameras()
                            
                            if available_cameras:
                                camera_index, backend = available_cameras[0]
                                success = st.session_state.camera_handler.start_camera(camera_index, backend)
                                
                                if success:
                                    st.session_state.camera_started = True
                                    st.success("Camera started successfully!")
                                else:
                                    st.error("Failed to start camera. Please check camera permissions.")
                            else:
                                st.error("No cameras found. Please check if your camera is connected and not being used by another application.")
            
            with col1_2:
                if st.button("⏹️ Stop Exercise"):
                    st.session_state.is_running = False
                    if st.session_state.camera_started:
                        st.session_state.camera_handler.stop_camera()
                        st.session_state.camera_started = False
            with col1_3:
                if st.button("📊 Save Session"):
                    st.success("Session data saved!")
            
            # Exercise timer
            if st.session_state.is_running:
                timer_placeholder = st.empty()
                start_time = time.time()
            
            # Camera feed (enhanced with your existing code)
            camera_placeholder = st.empty()
            
            if st.session_state.is_running and st.session_state.camera_started:
                # Display live camera feed with pose detection
                frame = st.session_state.camera_handler.read_frame()
                
                if frame is not None:
                    # Perform pose detection if MediaPipe is available
                    if MEDIAPIPE_AVAILABLE and hasattr(st.session_state, 'pose_detector'):
                        landmarks, annotated_frame = st.session_state.pose_detector.detect_pose(frame)
                        
                        # Perform exercise analysis if landmarks detected
                        analysis_result = None
                        if landmarks:
                            # Map exercise selection to analyzer function
                            exercise_map = {
                                "Cervical Flexion (Chin-to-chest)": "cervical_flexion",
                                "Cervical Extension (Look upward)": "cervical_extension", 
                                "Lateral Neck Tilt (Left and Right)": "lateral_tilt",
                                "Neck Rotation (Turn head left/right)": "rotation",
                                "Chin Tuck (Retract chin)": "chin_tuck"
                            }
                            
                            exercise_type = exercise_map.get(selected_exercise, "cervical_flexion")
                            
                            # Analyze the specific exercise
                            if exercise_type == "cervical_flexion":
                                analysis_result = st.session_state.exercise_analyzer.analyze_cervical_flexion(landmarks)
                            elif exercise_type == "cervical_extension":
                                analysis_result = st.session_state.exercise_analyzer.analyze_cervical_extension(landmarks)
                            elif exercise_type == "lateral_tilt":
                                analysis_result = st.session_state.exercise_analyzer.analyze_lateral_tilt(landmarks)
                            elif exercise_type == "rotation":
                                analysis_result = st.session_state.exercise_analyzer.analyze_rotation(landmarks)
                            elif exercise_type == "chin_tuck":
                                analysis_result = st.session_state.exercise_analyzer.analyze_chin_tuck(landmarks)
                            
                            # Add analysis overlay to frame
                            if analysis_result:
                                add_analysis_overlay(annotated_frame, analysis_result)
                    else:
                        # If MediaPipe not available, just show camera feed
                        annotated_frame = frame
                        analysis_result = None
                    
                    # Convert BGR to RGB for Streamlit
                    frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                    camera_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)
                    
                    # Display analysis results in sidebar if available
                    if analysis_result:
                        st.sidebar.subheader("📊 Exercise Analysis")
                        status_color = "🟢" if analysis_result['status'] == 'Good' else "🟡" if analysis_result['status'] in ['Too little', 'Too much'] else "🔴"
                        st.sidebar.markdown(f"{status_color} **Status:** {analysis_result['status']}")
                        if 'angle' in analysis_result:
                            st.sidebar.metric("Angle", f"{analysis_result['angle']:.1f}°")
                        if 'distance' in analysis_result:
                            st.sidebar.metric("Distance", f"{analysis_result['distance']:.3f}")
                        st.sidebar.info(f"💡 {analysis_result['feedback']}")
                else:
                    camera_placeholder.error("❌ Camera not available or disconnected")
            elif st.session_state.is_running:
                camera_placeholder.warning("⚠️ Camera not started. Click 'Start Exercise' to initialize camera.")
            else:
                camera_placeholder.info("📸 Click 'Start Exercise' to begin camera feed")
        
        with col2:
            st.subheader("📊 Real-time Feedback")
            
            # Session statistics
            if hasattr(st.session_state, 'progress_tracker'):
                stats = st.session_state.progress_tracker.get_session_stats()
                if stats:
                    st.metric("Session Duration", f"{stats.get('session_duration', 0):.1f}s")
                    st.metric("Accuracy", f"{stats.get('average_accuracy', 0):.1f}%")
                    st.metric("Measurements", stats.get('total_measurements', 0))
            
            # Exercise instructions
            st.subheader("📝 Current Exercise")
            exercise_instructions = {
                "Cervical Flexion (Chin-to-chest)": "Slowly lower your chin toward your chest. Keep your shoulders relaxed.",
                "Cervical Extension (Look upward)": "Gently tilt your head back and look upward. Don't overextend.",
                "Lateral Neck Tilt (Left and Right)": "Tilt your head to one side, bringing your ear toward your shoulder.",
                "Neck Rotation (Turn head left/right)": "Slowly turn your head to the left and right, looking over your shoulder.",
                "Chin Tuck (Retract chin)": "Pull your chin back, creating a double chin. Hold the position."
            }
            
            instruction = exercise_instructions.get(selected_exercise, "Follow the instructions and maintain proper form.")
            st.info(f"💡 {instruction}")
            
            # Exercise progress
            if st.session_state.is_running:
                st.success("🔴 Recording in progress...")
                
                # Add timer display
                if 'start_time' in locals():
                    current_time = time.time() - start_time
                    st.metric("Exercise Time", f"{current_time:.1f}s")
            else:
                st.info("⏸️ Ready to start")
    
    with tab2:
        st.subheader("📈 Progress Analytics")
        
        if hasattr(st.session_state, 'progress_tracker') and st.session_state.progress_tracker.exercise_data:
            # Progress visualization
            fig = st.session_state.progress_tracker.plot_progress()
            if fig:
                st.pyplot(fig)
            
            # Session statistics
            stats = st.session_state.progress_tracker.get_session_stats()
            if stats:
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                with col_stat1:
                    st.metric("Total Exercises", stats.get('exercises_performed', 0))
                with col_stat2:
                    st.metric("Overall Accuracy", f"{stats.get('average_accuracy', 0):.1f}%")
                with col_stat3:
                    st.metric("Total Time", f"{stats.get('session_duration', 0):.1f}s")
                
                # Detailed breakdown
                st.subheader("📋 Exercise Breakdown")
                for exercise, data in stats.get('by_exercise', {}).items():
                    with st.expander(f"{exercise} Details"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Repetitions", data['count'])
                            st.metric("Accuracy", f"{data['accuracy']:.1f}%")
                        with col2:
                            st.metric("Avg Measurement", f"{data['avg_measurement']:.1f}")
                            st.metric("Best Performance", f"{data['best_measurement']:.1f}")
        else:
            st.info("📊 Start exercising to see your progress data!")
    
    with tab3:
        st.subheader("🎯 Personalized Exercise Plans")
        
        # Exercise prescription interface
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**Available Programs:**")
            
            for level, program in st.session_state.prescription_system.prescriptions.items():
                with st.expander(f"{program['name']} ({level.title()})"):
                    st.markdown(f"**Duration:** {program['duration_weeks']} weeks")
                    st.markdown("**Exercises:**")
                    for exercise in program['exercises']:
                        st.markdown(f"- **{exercise['name']}**")
                        st.markdown(f"  - {exercise['sets']} sets × {exercise['reps']} reps")
                        st.markdown(f"  - Hold: {exercise['hold_time']}s")
                        st.markdown(f"  - Frequency: {exercise['frequency_per_week']}/week")
        
        with col2:
            st.markdown("**Weekly Schedule Preview:**")
            prescription = st.session_state.prescription_system.get_prescription(fitness_level)
            schedule = st.session_state.prescription_system.create_weekly_schedule(prescription)
            
            for day, exercises in schedule.items():
                if exercises:
                    st.markdown(f"**{day}:**")
                    for ex in exercises:
                        st.markdown(f"- {ex['exercise']}")

if __name__ == "__main__":
    main()