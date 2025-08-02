"""
Streamlit UI components for the cervical pose detection system.
"""
import streamlit as st
import numpy as np
from typing import Dict, List
import time

from ..core.models import ExerciseType, ExerciseResult, DetectionStatus, SystemConfig


class UIComponents:
    """Collection of reusable UI components"""
    
    @staticmethod
    def render_header():
        """Render the main application header"""
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="color: #2e8b57; font-size: 2.5rem; margin-bottom: 0.5rem;">
                🏥 Cervical Pose Detection System
            </h1>
            <p style="color: #666; font-size: 1.1rem;">
                Real-time cervical exercise detection and feedback
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_exercise_status_panel(exercise_results: Dict[ExerciseType, ExerciseResult], selected_exercise: ExerciseType = None):
        """Render the comprehensive exercise status panel"""
        
        # If specific exercise selected, show only that one
        if selected_exercise and selected_exercise in exercise_results:
            st.subheader(f"🎯 {selected_exercise.value}")
            result = exercise_results[selected_exercise]
            UIComponents._render_single_exercise_detailed(selected_exercise, result)
        else:
            # Show overview of all exercises
            st.subheader("🎯 All Exercises Overview")
            
            # Quick status grid
            cols = st.columns(len(exercise_results))
            for i, (exercise_type, result) in enumerate(exercise_results.items()):
                with cols[i]:
                    if result.status == DetectionStatus.DETECTED:
                        st.success(f"✅")
                        st.caption(f"{exercise_type.value[:15]}...")  # Truncate long names
                        st.caption(f"{result.confidence:.0%}")
                    elif result.status == DetectionStatus.CALIBRATING:
                        st.info(f"⏳")
                        st.caption(f"{exercise_type.value[:15]}...")
                        st.caption("Calibrating...")
                    elif result.status == DetectionStatus.READY:
                        st.info(f"⚡")
                        st.caption(f"{exercise_type.value[:15]}...")
                        st.caption("Ready")
                    else:
                        st.error(f"○")
                        st.caption(f"{exercise_type.value[:15]}...")
                        st.caption("Not detected")
            
            st.divider()
            
            # Show active exercises (detected or calibrating) with details
            active_exercises = [
                (exercise_type, result) for exercise_type, result in exercise_results.items()
                if result.detected or result.status == DetectionStatus.CALIBRATING
            ]
            
            if active_exercises:
                st.subheader("🔥 Active Exercises")
                for exercise_type, result in active_exercises:
                    UIComponents._render_single_exercise_status(exercise_type, result)
            else:
                st.info("💡 Perform an exercise to see detailed feedback here")
    
    @staticmethod
    def _render_single_exercise_detailed(exercise_type: ExerciseType, result: ExerciseResult):
        """Render detailed view for a single exercise"""
        
        # Large status indicator with emphasis
        if result.status == DetectionStatus.DETECTED:
            st.success(f"🎉 **EXERCISE DETECTED!**")
            st.progress(result.confidence, text=f"Confidence: {result.confidence:.1%}")
            
            # Large congratulatory message
            st.markdown(f"### 💪 Great job! Keep holding the position!")
            
        elif result.status == DetectionStatus.CALIBRATING:
            st.info(f"⏳ **CALIBRATING SYSTEM...**")
            # Show progress if available
            if hasattr(result, 'progress') and result.progress:
                st.progress(result.progress / 100.0, text=f"Calibration Progress: {result.progress:.0f}%")
            st.markdown("### 🧘‍♀️ Please stay in neutral position")
            
        elif result.status == DetectionStatus.READY:
            st.info(f"⚡ **READY FOR DETECTION**")
            st.markdown("### 🚀 You can start the exercise now!")
            
        elif result.status == DetectionStatus.ERROR:
            st.error(f"❌ **SYSTEM ERROR**")
            st.markdown("### 🔧 Please check camera and lighting")
            
        else:
            st.warning(f"👀 **LOOKING FOR EXERCISE...**")
            st.markdown("### 🎯 Perform the exercise to get feedback")
        
        # Status message with larger text - ONLY for selected exercise
        if result.status_message:
            st.markdown(f"#### 📝 {result.status_message}")
        
        # Exercise instructions - ONLY for selected exercise
        instructions = UIComponents._get_exercise_instructions(exercise_type)
        st.info(f"**💡 How to perform:** {instructions}")
        
        # Show tips for better detection
        tips = UIComponents._get_exercise_tips(exercise_type)
        with st.expander("🎯 Tips for Better Detection", expanded=False):
            st.markdown(tips)
        
        # Metrics in expandable section - ONLY for selected exercise
        if result.metrics:
            with st.expander("📊 Technical Metrics", expanded=False):
                UIComponents._render_exercise_metrics(result.metrics)
    
    @staticmethod
    def _get_exercise_tips(exercise_type: ExerciseType) -> str:
        """Get tips for better detection of each exercise"""
        tips = {
            ExerciseType.CERVICAL_FLEXION: """
            - Move slowly and smoothly
            - Lower your chin as far as comfortable
            - Keep your shoulders relaxed
            - Hold the position for 2-3 seconds
            - Feel the stretch in the back of your neck
            """,
            ExerciseType.CERVICAL_EXTENSION: """
            - Tilt your head back gently
            - Don't force the movement
            - Keep your mouth closed
            - Look toward the ceiling
            - Stop if you feel dizzy
            """,
            ExerciseType.LATERAL_NECK_TILT: """
            - Keep your shoulders level
            - Bring ear toward shoulder, not shoulder to ear
            - Don't twist your head
            - Feel the stretch on the side of your neck
            - Hold for 2-3 seconds before returning
            """,
            ExerciseType.NECK_ROTATION: """
            - Turn your head slowly
            - Keep your chin level
            - Look as far as comfortable
            - Don't force the rotation
            - Return to center between sides
            """,
            ExerciseType.CHIN_TUCK: """
            - Pull your chin straight back
            - Create a "double chin" effect
            - Keep your head level
            - Don't tilt up or down
            - Hold for 5 seconds
            """
        }
        return tips.get(exercise_type, "Perform the exercise slowly and smoothly.")
    
    @staticmethod
    def _get_exercise_instructions(exercise_type: ExerciseType) -> str:
        """Get instructions for each exercise"""
        instructions = {
            ExerciseType.CERVICAL_FLEXION: "Slowly lower your chin toward your chest. Feel the stretch in the back of your neck.",
            ExerciseType.CERVICAL_EXTENSION: "Gently tilt your head back to look upward. Don't force the movement.",
            ExerciseType.LATERAL_NECK_TILT: "Tilt your head to bring your ear toward your shoulder. Keep shoulders level.",
            ExerciseType.NECK_ROTATION: "Turn your head to look left or right. Move slowly and smoothly.",
            ExerciseType.CHIN_TUCK: "Pull your chin straight back to create a 'double chin'. Hold briefly."
        }
        return instructions.get(exercise_type, "Perform the exercise slowly and smoothly.")
    @staticmethod
    def _render_single_exercise_status(exercise_type: ExerciseType, result: ExerciseResult):
        """Render compact status for a single exercise"""
        # Create container for this exercise
        container = st.container()
        
        with container:
            # Choose styling based on status
            if result.status == DetectionStatus.DETECTED:
                st.success(f"✅ **{exercise_type.value}** - DETECTED!")
                if result.confidence > 0:
                    st.progress(result.confidence, text=f"Confidence: {result.confidence:.1%}")
            
            elif result.status == DetectionStatus.CALIBRATING:
                st.info(f"⏳ **{exercise_type.value}** - Calibrating...")
                if hasattr(result, 'progress') and result.progress:
                    st.progress(result.progress / 100.0, text=f"Progress: {result.progress:.0f}%")
            
            elif result.status == DetectionStatus.READY:
                st.info(f"⚡ **{exercise_type.value}** - Ready for detection")
            
            elif result.status == DetectionStatus.ERROR:
                st.error(f"❌ **{exercise_type.value}** - Error")
            
            else:
                st.warning(f"○ **{exercise_type.value}** - Not detected")
            
            # Show status message if available
            if result.status_message:
                st.caption(f"📝 {result.status_message}")
            
            st.divider()
    
    @staticmethod
    def _render_exercise_metrics(metrics: dict):
        """Render detailed metrics for an exercise"""
        cols = st.columns(min(len(metrics), 3))
        
        for i, (key, value) in enumerate(metrics.items()):
            col = cols[i % len(cols)]
            with col:
                if isinstance(value, (int, float)):
                    st.metric(key.replace('_', ' ').title(), f"{value:.3f}")
                else:
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    
    @staticmethod
    def render_sidebar_controls(config: SystemConfig) -> dict:
        """Render sidebar controls and return control values"""
        st.sidebar.header("🎛️ Control Panel")
        
        # Camera settings
        st.sidebar.subheader("📹 Camera Settings")
        camera_index = st.sidebar.selectbox(
            "Camera Source",
            options=[0, 1, 2],
            format_func=lambda x: f"Camera {x}",
            help="Select which camera to use for detection"
        )
        
        # Exercise selection
        st.sidebar.subheader("🎯 Exercise Selection")
        
        # Dropdown for focused exercise with exact options requested
        exercise_options = [
            "All Exercises",
            "Cervical Flexion (Chin-to-chest)",
            "Cervical Extension (Look upward)", 
            "Lateral Neck Tilt (Left and Right)",
            "Neck Rotation (Turn head left/right)",
            "Chin Tuck (Retract chin)"
        ]
        
        selected_exercise_name = st.sidebar.selectbox(
            "Focus on Exercise",
            options=exercise_options,
            help="Select a specific exercise to focus on, or 'All Exercises' for overview"
        )
        
        # Convert back to enum if specific exercise selected
        focused_exercise = None
        if selected_exercise_name != "All Exercises":
            # Map display names to enum values
            exercise_mapping = {
                "Cervical Flexion (Chin-to-chest)": ExerciseType.CERVICAL_FLEXION,
                "Cervical Extension (Look upward)": ExerciseType.CERVICAL_EXTENSION,
                "Lateral Neck Tilt (Left and Right)": ExerciseType.LATERAL_NECK_TILT,
                "Neck Rotation (Turn head left/right)": ExerciseType.NECK_ROTATION,
                "Chin Tuck (Retract chin)": ExerciseType.CHIN_TUCK
            }
            focused_exercise = exercise_mapping.get(selected_exercise_name)
        
        # Exercise monitoring toggles
        st.sidebar.caption("Enable/Disable Exercises:")
        selected_exercises = []
        
        # Add "Select All" option
        select_all = st.sidebar.checkbox("Monitor All Exercises", value=True)
        
        for exercise_type in ExerciseType:
            default_checked = select_all
            is_checked = st.sidebar.checkbox(
                f"Monitor {exercise_type.value}",
                value=default_checked,
                key=f"exercise_{exercise_type.name}",
                disabled=select_all
            )
            
            if is_checked or select_all:
                selected_exercises.append(exercise_type)
        
        # Control buttons
        st.sidebar.subheader("🎮 Controls")
        
        button_col1, button_col2 = st.sidebar.columns(2)
        
        with button_col1:
            start_button = st.button("▶️ Start", use_container_width=True, type="primary")
        
        with button_col2:
            stop_button = st.button("⏹️ Stop", use_container_width=True)
        
        reset_button = st.sidebar.button(
            "🔄 Reset Calibration", 
            use_container_width=True,
            help="Reset all exercise baselines and recalibrate"
        )
        
        # Performance settings
        st.sidebar.subheader("⚙️ Performance Settings")
        
        fps_limit = st.sidebar.slider(
            "FPS Limit",
            min_value=5,
            max_value=30,
            value=config.fps_limit,
            help="Limit frames per second to reduce CPU usage"
        )
        
        # Advanced settings
        with st.sidebar.expander("🔧 Advanced Settings"):
            detection_confidence = st.slider(
                "Detection Confidence",
                min_value=0.1,
                max_value=1.0,
                value=config.min_detection_confidence,
                step=0.05,
                help="Minimum confidence for pose detection"
            )
            
            tracking_confidence = st.slider(
                "Tracking Confidence",
                min_value=0.1,
                max_value=1.0,
                value=config.min_tracking_confidence,
                step=0.05,
                help="Minimum confidence for pose tracking"
            )
            
            calibration_frames = st.slider(
                "Calibration Frames",
                min_value=10,
                max_value=30,
                value=config.calibration_frames,
                help="Number of frames for baseline calibration"
            )
        
        return {
            'camera_index': camera_index,
            'selected_exercises': selected_exercises,
            'focused_exercise': focused_exercise,
            'start_button': start_button,
            'stop_button': stop_button,
            'reset_button': reset_button,
            'fps_limit': fps_limit,
            'detection_confidence': detection_confidence,
            'tracking_confidence': tracking_confidence,
            'calibration_frames': calibration_frames
        }
    
    @staticmethod
    def render_system_stats(stats: dict):
        """Render system performance statistics"""
        st.subheader("📊 System Performance")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "FPS", 
                f"{stats.get('fps', 0):.1f}",
                help="Frames processed per second"
            )
        
        with col2:
            st.metric(
                "Total Frames", 
                stats.get('frame_count', 0),
                help="Total frames processed this session"
            )
        
        with col3:
            session_duration = stats.get('session_duration', 0)
            minutes = int(session_duration // 60)
            seconds = int(session_duration % 60)
            st.metric(
                "Session Time", 
                f"{minutes:02d}:{seconds:02d}",
                help="Duration of current session"
            )
        
        with col4:
            calibrated = stats.get('calibrated_detectors', 0)
            total = stats.get('total_detectors', 0)
            st.metric(
                "Calibration", 
                f"{calibrated}/{total}",
                help="Calibrated detectors / Total detectors"
            )
    
    @staticmethod
    def render_instructions():
        """Render detailed instructions"""
        with st.expander("📖 How to Use This System", expanded=False):
            st.markdown("""
            ### Getting Started
            
            1. **Position Yourself**
               - Sit or stand facing the camera
               - Ensure your head and shoulders are clearly visible
               - Maintain good lighting on your face
            
            2. **Calibration Process**
               - Click the "Start" button to begin
               - Stay in a neutral position for 15 frames (~1 second)
               - Wait for all exercises to show "Ready for detection"
            
            3. **Perform Exercises**
               - Perform each exercise slowly and deliberately
               - Hold each position briefly for better detection
               - Follow the real-time feedback messages
            
            ### Exercise Descriptions
            
            #### 🔽 Cervical Flexion
            - **Movement**: Lower your chin toward your chest
            - **Purpose**: Stretches the back of the neck
            - **Tip**: Move slowly and feel the stretch
            
            #### 🔼 Cervical Extension  
            - **Movement**: Gently tilt your head back to look upward
            - **Purpose**: Stretches the front of the neck
            - **Tip**: Don't force the movement, go to comfortable range
            
            #### ↔️ Lateral Neck Tilt
            - **Movement**: Tilt your head to bring ear toward shoulder
            - **Purpose**: Stretches the side of the neck
            - **Tip**: Keep shoulders relaxed and level
            
            #### 🔄 Neck Rotation
            - **Movement**: Turn your head to look left or right
            - **Purpose**: Improves neck mobility
            - **Tip**: Turn as far as comfortable, don't force
            
            #### 🎯 Chin Tuck
            - **Movement**: Pull your chin straight back
            - **Purpose**: Strengthens deep neck muscles
            - **Tip**: Create a "double chin" effect
            
            ### Understanding the Feedback
            
            - **✅ Green**: Exercise correctly detected - great job!
            - **⏳ Yellow**: System is calibrating - stay still
            - **○ Gray**: Exercise not detected - try adjusting movement
            - **❌ Red**: Error or pose not visible - check camera
            
            ### Troubleshooting
            
            - **Poor Detection**: Check lighting and camera angle
            - **Calibration Issues**: Stay very still during calibration
            - **No Pose Visible**: Ensure full head/shoulders are in frame
            - **Reset Needed**: Use "Reset Calibration" button if needed
            """)
    
    @staticmethod
    def render_ready_state_instructions():
        """Render instructions when system is not running"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            ### 🚀 Ready to Start
            
            **Before You Begin:**
            1. Select your camera from the sidebar
            2. Choose exercises to monitor
            3. Adjust performance settings if needed
            4. Click **Start** to begin detection
            
            **Position yourself so your head and shoulders are clearly visible in the camera.**
            """)
        
        with col2:
            st.success("""
            ### 💡 Pro Tips
            
            **For Best Results:**
            - Use good lighting (face the light source)
            - Keep background simple and uncluttered
            - Wear contrasting clothing (avoid white/black)
            - Maintain steady position during calibration
            
            **The system will calibrate automatically when you start.**
            """)


class SessionManager:
    """Manages Streamlit session state for the application"""
    
    @staticmethod
    def initialize_session_state():
        """Initialize all required session state variables"""
        defaults = {
            'running': False,
            'video_processor': None,
            'system_config': SystemConfig(),
            'session_stats': {},
            'last_exercise_results': {},
            'calibration_complete': False
        }
        
        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    @staticmethod
    def update_config_from_controls(controls: dict):
        """Update system config based on user controls"""
        if 'system_config' in st.session_state:
            config = st.session_state.system_config
            config.fps_limit = controls['fps_limit']
            config.min_detection_confidence = controls['detection_confidence']
            config.min_tracking_confidence = controls['tracking_confidence']
            config.calibration_frames = controls['calibration_frames']
