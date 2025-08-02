#!/usr/bin/env python3
"""Quick test to verify all imports work"""

print("Testing imports...")

try:
    import numpy as np
    print(f"✅ NumPy: {np.__version__}")
    if np.__version__.startswith('2.'):
        print("⚠️  WARNING: NumPy 2.x detected - may cause conflicts")
    else:
        print("✅ NumPy version is compatible")
except Exception as e:
    print(f"❌ NumPy error: {e}")

try:
    import streamlit as st
    print("✅ Streamlit imported successfully")
except Exception as e:
    print(f"❌ Streamlit error: {e}")

try:
    import mediapipe as mp
    print(f"✅ MediaPipe: {mp.__version__}")
except Exception as e:
    print(f"❌ MediaPipe error: {e}")

try:
    import cv2
    print(f"✅ OpenCV: {cv2.__version__}")
except Exception as e:
    print(f"❌ OpenCV error: {e}")

# Test MediaPipe functionality
try:
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    print("✅ MediaPipe Pose initialized successfully")
except Exception as e:
    print(f"❌ MediaPipe Pose error: {e}")

print("\n🎯 Test complete!")