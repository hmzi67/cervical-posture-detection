"""
Main Streamlit application for cervical pose detection system.
Production-ready with proper error handling and modular architecture.
"""
import streamlit as st
import cv2
import time
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.models import SystemConfig
from src.core.video_processor import VideoProcessor
from src.ui.components import UIComponents, SessionManager


def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Cervical Pose Detection System",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/hmzi67/cervical-posture-detection.git',
            'Report a bug': 'https://github.com/hmzi67/cervical-posture-detection/issues',
            'About': """
            # Cervical Pose Detection System
            
            A real-time system for detecting and providing feedback on cervical exercises
            using computer vision and pose estimation.
            
            **Features:**
            - Real-time pose detection
            - 5 cervical exercise types
            - Automatic calibration
            - Performance feedback
            """
        }
    )


def apply_custom_styles():
    """Apply custom CSS styles"""
    st.markdown("""
    <style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        color: #2e8b57;
        font-size: 2.5rem;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Metric styling */
    [data-testid="metric-container"] {
        background-color: rgba(28, 131, 225, 0.1);
        border: 1px solid rgba(28, 131, 225, 0.2);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Success/Error styling */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px;
        border-left: 5px solid;
        margin: 1rem 0;
    }
    
    /* Video container */
    .video-container {
        border: 3px solid #2e8b57;
        border-radius: 15px;
        padding: 10px;
        background: linear-gradient(145deg, #f0f0f0, #ffffff);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background-color: #2e8b57;
    }
    </style>
    """, unsafe_allow_html=True)


def handle_video_processing(video_processor: VideoProcessor, controls: dict):
    """Handle the main video processing loop"""
    # Create layout
    col1, col2 = st.columns([3, 2])  # Give more space to camera, less to feedback
    
    with col1:
        st.markdown('<div class="video-container">', unsafe_allow_html=True)
        st.subheader("📹 Live Camera Feed")
        video_placeholder = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        status_placeholder = st.empty()
    
    # Performance monitoring
    performance_placeholder = st.empty()
    
    # Initialize camera
    try:
        cap = cv2.VideoCapture(controls['camera_index'])
        
        if not cap.isOpened():
            st.error(f"❌ Could not open camera {controls['camera_index']}")
            st.info("💡 Try selecting a different camera from the sidebar")
            st.session_state.running = False
            return
        
        # Configure camera
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, st.session_state.system_config.video_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, st.session_state.system_config.video_height)
        cap.set(cv2.CAP_PROP_FPS, controls['fps_limit'])
        
        # Frame timing
        frame_time = 1.0 / controls['fps_limit']
        
        # Processing loop
        while st.session_state.running:
            loop_start = time.time()
            
            # Capture frame
            ret, frame = cap.read()
            if not ret:
                st.error("❌ Failed to capture frame from camera")
                break
            
            # Process frame
            try:
                processed_frame, exercise_results = video_processor.process_frame(frame)
                
                # Convert BGR to RGB for Streamlit
                display_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                
                # Update displays
                video_placeholder.image(
                    display_frame, 
                    channels="RGB", 
                    use_column_width=True,
                    caption="Real-time pose detection and exercise feedback"
                )
                
                # Update exercise status
                with status_placeholder.container():
                    UIComponents.render_exercise_status_panel(
                        exercise_results, 
                        controls.get('focused_exercise')
                    )
                
                # Update performance stats
                stats = video_processor.get_system_stats()
                st.session_state.session_stats = stats
                
                with performance_placeholder.container():
                    UIComponents.render_system_stats(stats)
                
                # Store results for potential export
                st.session_state.last_exercise_results = exercise_results
                
            except Exception as e:
                st.error(f"❌ Frame processing error: {str(e)}")
                st.info("💡 Try resetting calibration or restarting the camera")
            
            # Frame rate control
            elapsed = time.time() - loop_start
            sleep_time = max(0, frame_time - elapsed)
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    except Exception as e:
        st.error(f"❌ Camera initialization error: {str(e)}")
        st.info("💡 Check camera permissions and connections")
    
    finally:
        # Cleanup
        if 'cap' in locals() and cap.isOpened():
            cap.release()
        st.session_state.running = False


def main():
    """Main application function"""
    # Configure page
    configure_page()
    apply_custom_styles()
    
    # Initialize session state
    SessionManager.initialize_session_state()
    
    # Render header
    UIComponents.render_header()
    
    # Update config from previous session if needed
    if st.session_state.system_config is None:
        st.session_state.system_config = SystemConfig()
    
    # Render sidebar controls
    controls = UIComponents.render_sidebar_controls(st.session_state.system_config)
    
    # Update config from controls
    SessionManager.update_config_from_controls(controls)
    
    # Handle control actions
    if controls['start_button'] and not st.session_state.running:
        st.session_state.running = True
        
        # Initialize video processor with updated config
        st.session_state.video_processor = VideoProcessor(st.session_state.system_config)
        
        st.success("🚀 Starting cervical pose detection system...")
        time.sleep(1)  # Brief pause for user feedback
        st.rerun()
    
    if controls['stop_button'] and st.session_state.running:
        st.session_state.running = False
        
        # Cleanup video processor
        if st.session_state.video_processor:
            st.session_state.video_processor.cleanup()
        
        st.info("⏹️ Detection stopped")
        st.rerun()
    
    if controls['reset_button']:
        if st.session_state.video_processor:
            st.session_state.video_processor.reset_baselines()
            st.success("🔄 Calibration reset successfully!")
        else:
            st.warning("⚠️ Start the system first before resetting calibration")
    
    # Main content based on running state
    if st.session_state.running and st.session_state.video_processor:
        # Show video processing interface
        handle_video_processing(st.session_state.video_processor, controls)
    
    else:
        # Show ready state instructions
        UIComponents.render_ready_state_instructions()
        
        # Show previous session stats if available
        if st.session_state.session_stats:
            with st.expander("📊 Previous Session Statistics"):
                UIComponents.render_system_stats(st.session_state.session_stats)
    
    # Always show instructions
    UIComponents.render_instructions()
    
    # Footer with additional info
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🏥 Cervical Pose Detection System | Built with ❤️ using Streamlit & MediaPipe</p>
        <p><small>For best results, ensure good lighting and keep your head and shoulders in frame</small></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"❌ Application error: {str(e)}")
        st.info("💡 Please refresh the page and try again")
        st.exception(e)  # Show full traceback in development
