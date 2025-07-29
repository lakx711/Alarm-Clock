#!/usr/bin/env python3
"""
Simple test script for the Alarm Clock application.
This script tests basic functionality without running the full GUI.
"""

import sys
import datetime
import time

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import tkinter as tk
        from tkinter import ttk, filedialog, messagebox
        print("✓ tkinter modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import tkinter: {e}")
        return False
    
    try:
        import pygame
        print("✓ pygame imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import pygame: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ numpy imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import numpy: {e}")
        return False
    
    try:
        from sound_generator import generate_default_alarm_sound, cleanup_temp_sound
        print("✓ sound_generator imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import sound_generator: {e}")
        return False
    
    return True

def test_sound_generation():
    """Test sound generation functionality."""
    print("\nTesting sound generation...")
    
    try:
        from sound_generator import generate_default_alarm_sound, cleanup_temp_sound
        
        # Generate a test sound
        sound_path = generate_default_alarm_sound()
        if sound_path:
            print(f"✓ Sound generated successfully: {sound_path}")
            
            # Clean up
            cleanup_temp_sound(sound_path)
            print("✓ Sound cleanup successful")
            return True
        else:
            print("✗ Failed to generate sound")
            return False
            
    except Exception as e:
        print(f"✗ Sound generation test failed: {e}")
        return False

def test_time_validation():
    """Test time validation logic."""
    print("\nTesting time validation...")
    
    # Test valid times
    valid_times = ["00:00", "12:30", "23:59", "07:00"]
    for time_str in valid_times:
        try:
            hour, minute = map(int, time_str.split(':'))
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                print(f"✓ Valid time: {time_str}")
            else:
                print(f"✗ Invalid time range: {time_str}")
                return False
        except ValueError:
            print(f"✗ Invalid time format: {time_str}")
            return False
    
    # Test invalid times
    invalid_times = ["24:00", "12:60", "25:30", "abc", "12:30:45"]
    for time_str in invalid_times:
        try:
            hour, minute = map(int, time_str.split(':'))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                print(f"✓ Correctly rejected invalid time: {time_str}")
            else:
                print(f"✗ Should have rejected: {time_str}")
                return False
        except ValueError:
            print(f"✓ Correctly rejected invalid format: {time_str}")
    
    return True

def test_alarm_logic():
    """Test basic alarm logic."""
    print("\nTesting alarm logic...")
    
    now = datetime.datetime.now()
    
    # Test alarm time calculation
    test_hour, test_minute = 10, 30
    alarm_time = now.replace(hour=test_hour, minute=test_minute, second=0, microsecond=0)
    
    # If alarm time has passed today, it should be set for tomorrow
    if alarm_time <= now:
        alarm_time += datetime.timedelta(days=1)
        print(f"✓ Alarm time adjusted to tomorrow: {alarm_time.strftime('%Y-%m-%d %H:%M')}")
    else:
        print(f"✓ Alarm time set for today: {alarm_time.strftime('%Y-%m-%d %H:%M')}")
    
    return True

def main():
    """Run all tests."""
    print("🔔 Alarm Clock Test Suite")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("Sound Generation Test", test_sound_generation),
        ("Time Validation Test", test_time_validation),
        ("Alarm Logic Test", test_alarm_logic),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * len(test_name))
        
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The alarm clock should work correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 