"""
Test runner for the Cervical Pose Detection System.

Run all tests with: python -m pytest tests/
Run specific test file: python tests/test_runner.py
"""
import unittest
import sys
import os

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import test modules
from tests.test_detection_system import *
from tests.test_geometry_utils import *
from tests.test_models import *
from tests.test_video_processor import *


def run_all_tests():
    """Run all test suites and provide comprehensive reporting"""
    
    print("="*70)
    print("CERVICAL POSE DETECTION SYSTEM - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    # Define test modules and their descriptions
    test_modules = [
        ('test_models', 'Data Models and Configuration'),
        ('test_geometry_utils', 'Geometry Utilities and Math Functions'),
        ('test_detection_system', 'Exercise Detection System'),
        ('test_video_processor', 'Video Processing and MediaPipe Integration')
    ]
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    
    # Run each test module
    for module_name, description in test_modules:
        print(f"\n{'-'*50}")
        print(f"Running: {description}")
        print(f"Module: {module_name}")
        print(f"{'-'*50}")
        
        # Load and run tests for this module
        suite = unittest.TestLoader().loadTestsFromName(module_name)
        runner = unittest.TextTestRunner(verbosity=1, stream=sys.stdout)
        result = runner.run(suite)
        
        # Accumulate results
        total_tests += result.testsRun
        total_failures += len(result.failures)
        total_errors += len(result.errors)
        
        # Show module summary
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
        print(f"\nModule Summary:")
        print(f"  Tests: {result.testsRun}")
        print(f"  Failures: {len(result.failures)}")
        print(f"  Errors: {len(result.errors)}")
        print(f"  Success Rate: {success_rate:.1f}%")
        
        # Show failures and errors if any
        if result.failures:
            print(f"\n  FAILURES:")
            for test, traceback in result.failures:
                print(f"    - {test}: {traceback.split('AssertionError:')[-1].strip() if 'AssertionError:' in traceback else 'See details above'}")
        
        if result.errors:
            print(f"\n  ERRORS:")
            for test, traceback in result.errors:
                print(f"    - {test}: {traceback.split('Exception:')[-1].strip() if 'Exception:' in traceback else 'See details above'}")
    
    # Overall summary
    print(f"\n{'='*70}")
    print(f"OVERALL TEST RESULTS")
    print(f"{'='*70}")
    
    overall_success_rate = ((total_tests - total_failures - total_errors) / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Total Tests Run: {total_tests}")
    print(f"Total Failures: {total_failures}")
    print(f"Total Errors: {total_errors}")
    print(f"Overall Success Rate: {overall_success_rate:.1f}%")
    
    # Status determination
    if total_failures == 0 and total_errors == 0:
        status = "✅ ALL TESTS PASSED!"
        print(f"\n{status}")
    elif total_failures == 0:
        status = "⚠️  SOME ERRORS (but no failures)"
        print(f"\n{status}")
    else:
        status = "❌ SOME TESTS FAILED"
        print(f"\n{status}")
    
    print("\nTest Coverage Areas:")
    print("  ✅ Data Models and Enums")
    print("  ✅ Geometry Calculations")
    print("  ✅ Exercise Detection Logic")
    print("  ✅ Video Processing Pipeline")
    print("  ✅ MediaPipe Integration")
    print("  ✅ Error Handling")
    print("  ✅ Configuration Management")
    print("  ✅ System Integration")
    
    print(f"\n{'='*70}")
    
    return total_failures == 0 and total_errors == 0


def run_quick_tests():
    """Run a subset of critical tests for quick validation"""
    
    print("="*50)
    print("QUICK TEST SUITE - CRITICAL FUNCTIONALITY")
    print("="*50)
    
    # Define critical test classes
    critical_tests = [
        'TestExerciseType',
        'TestDetectionStatus', 
        'TestSystemConfig',
        'TestGeometryUtils',
        'TestCervicalFlexionDetector',
        'TestVideoProcessor'
    ]
    
    suite = unittest.TestSuite()
    
    for test_class_name in critical_tests:
        try:
            test_class = globals()[test_class_name]
            tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
            suite.addTests(tests)
        except KeyError:
            print(f"Warning: Test class {test_class_name} not found")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    
    print(f"\nQuick Test Summary:")
    print(f"Tests: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    return len(result.failures) == 0 and len(result.errors) == 0


def run_performance_tests():
    """Run performance-focused tests"""
    
    print("="*50)
    print("PERFORMANCE TEST SUITE")
    print("="*50)
    
    # These would be performance-specific tests
    # For now, we'll run tests that check performance metrics
    
    performance_test_classes = [
        'TestVideoProcessor',  # Includes performance monitoring tests
        'TestExerciseDetectionSystem'  # Includes system stats tests
    ]
    
    suite = unittest.TestSuite()
    
    for test_class_name in performance_test_classes:
        try:
            test_class = globals()[test_class_name]
            tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
            suite.addTests(tests)
        except KeyError:
            print(f"Warning: Test class {test_class_name} not found")
    
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    
    print(f"\nPerformance Test Summary:")
    print(f"Tests: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    return len(result.failures) == 0 and len(result.errors) == 0


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run Cervical Pose Detection System Tests')
    parser.add_argument('--quick', action='store_true', help='Run quick test suite only')
    parser.add_argument('--performance', action='store_true', help='Run performance tests only')
    parser.add_argument('--all', action='store_true', help='Run all tests (default)')
    
    args = parser.parse_args()
    
    if args.quick:
        success = run_quick_tests()
    elif args.performance:
        success = run_performance_tests()
    else:
        success = run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
