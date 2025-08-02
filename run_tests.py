#!/usr/bin/env python3
"""
Simple test runner for Cervical Pose Detection System.

This script can be run directly:
    python run_tests.py

Or with pytest:
    python -m pytest tests/ -v
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def main():
    """Run tests using pytest if available, otherwise use unittest"""
    
    print("🧪 Cervical Pose Detection System - Test Suite")
    print("=" * 50)
    
    # Check if required modules are available
    try:
        import numpy
        import cv2
        import mediapipe
        print("✅ All dependencies available")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies: pip install -r requirements.txt")
        return 1
    
    # Try to run pytest first
    try:
        import pytest
        print("🚀 Running tests with pytest...")
        exit_code = pytest.main([
            'tests/',
            '-v',
            '--tb=short',
            '--no-header'
        ])
        return exit_code
    except ImportError:
        print("📝 pytest not available, using unittest...")
        
        # Fallback to unittest
        import unittest
        
        # Discover and run tests
        loader = unittest.TestLoader()
        start_dir = os.path.join(project_root, 'tests')
        suite = loader.discover(start_dir, pattern='test_*.py')
        
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        # Return appropriate exit code
        return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
