"""
Main Streamlit application for Cervical Posture Detection
"""
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile
import os

# Set page config
st.set_page_config(
    page_title="Cervical Posture Detection App",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🏥 Cervical Posture Detection App")
    st.markdown("### Real-time posture monitoring for cervical physiotherapy exercises")
    
    # Sidebar for exercise selection
    st.sidebar.title("Exercise Selection")
    exercise_options = [
        "Cervical Flexion (Chin-to-chest)",
        "Cervical Extension (Look upward)",
        "Lateral Neck Tilt (Left and Right)",
        "Neck Rotation (Turn head left/right)",
        "Chin Tuck (Retract chin)"
    ]
    
    selected_exercise = st.sidebar.selectbox(
        "Choose an exercise:",
        exercise_options
    )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📹 Camera Feed")
        # Placeholder for camera feed
        camera_placeholder = st.empty()
        
        # Start/Stop buttons
        start_button = st.button("Start Exercise")
        stop_button = st.button("Stop Exercise")
        
        if start_button:
            st.success(f"Starting {selected_exercise}")
            # TODO: Implement camera capture and pose detection
            
    with col2:
        st.subheader("📊 Real-time Feedback")
        
        # Posture status
        st.metric("Posture Status", "Good", "✅")
        
        # Exercise progress
        progress_bar = st.progress(0)
        st.write("Exercise Progress: 0%")
        
        # Angle measurements
        st.subheader("📐 Measurements")
        st.metric("Head Tilt Angle", "15°", "2°")
        st.metric("Neck Rotation", "5°", "-3°")
        
        # Instructions
        st.subheader("📝 Instructions")
        exercise_instructions = {
            "Cervical Flexion (Chin-to-chest)": "Slowly lower your chin toward your chest. Keep your shoulders relaxed and back straight.",
            "Cervical Extension (Look upward)": "Gently tilt your head back and look upward. Don't strain your neck.",
            "Lateral Neck Tilt (Left and Right)": "Slowly tilt your head to one side, bringing your ear toward your shoulder. Then repeat on the other side.",
            "Neck Rotation (Turn head left/right)": "Turn your head slowly from left to right and back to center. Keep movements smooth and controlled.",
            "Chin Tuck (Retract chin)": "Pull your chin back toward your neck, creating a 'double chin' position. Hold for 5 seconds."
        }
        
        st.info(exercise_instructions[selected_exercise])
        
        # Exercise-specific tips
        st.subheader("💡 Tips")
        exercise_tips = {
            "Cervical Flexion (Chin-to-chest)": "• Don't force the movement\n• Stop if you feel pain\n• Hold for 5-10 seconds",
            "Cervical Extension (Look upward)": "• Move slowly and gently\n• Don't hyperextend\n• Support with hands if needed",
            "Lateral Neck Tilt (Left and Right)": "• Keep shoulders level\n• Don't lift shoulder to ear\n• Feel stretch on opposite side",
            "Neck Rotation (Turn head left/right)": "• Turn only as far as comfortable\n• Keep chin level\n• Move slowly without jerking",
            "Chin Tuck (Retract chin)": "• Keep eyes looking forward\n• Don't tilt head up or down\n• Imagine making a double chin"
        }
        
        st.markdown(exercise_tips[selected_exercise])

if __name__ == "__main__":
    main()