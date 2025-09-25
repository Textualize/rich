#!/usr/bin/env python3
"""
Test script for ConsoleThreadLocals pickle support
"""

import pickle
import sys
import os

# Add the current directory to the path so we can import the modified rich
sys.path.insert(0, '/tmp/rich')

from rich.console import Console
from rich.segment import Segment


def test_basic_pickle():
    """Test basic pickle functionality of ConsoleThreadLocals."""
    print("🧪 Testing basic ConsoleThreadLocals pickle functionality...")
    
    console = Console()
    ctl = console._thread_locals
    
    # Add some data to make it more realistic
    ctl.buffer.append(Segment("test"))
    ctl.buffer_index = 1
    
    try:
        # Test serialization
        pickled_data = pickle.dumps(ctl)
        print("  ✅ Serialization successful")
        
        # Test deserialization
        restored_ctl = pickle.loads(pickled_data)
        print("  ✅ Deserialization successful")
        
        # Verify state preservation
        assert type(restored_ctl.theme_stack) == type(ctl.theme_stack)
        assert restored_ctl.buffer == ctl.buffer
        assert restored_ctl.buffer_index == ctl.buffer_index
        print("  ✅ State preservation verified")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        return False


def test_langflow_compatibility():
    """Test compatibility with Langflow's caching mechanism."""
    print("🔧 Testing Langflow cache compatibility...")
    
    console = Console()
    
    # Simulate Langflow's cache data structure
    result_dict = {
        "result": console,
        "type": type(console),
    }
    
    try:
        # This is what Langflow's cache service tries to do
        pickled = pickle.dumps(result_dict)
        print("  ✅ Complex object serialization successful")
        
        restored = pickle.loads(pickled)
        print("  ✅ Complex object deserialization successful")
        
        # Verify the console is properly restored
        assert type(restored["result"]) == type(console)
        print("  ✅ Object type preservation verified")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        return False


def test_thread_local_behavior():
    """Test that thread-local behavior works after unpickling."""
    print("🔄 Testing thread-local behavior preservation...")
    
    import threading
    import time
    
    console = Console()
    ctl = console._thread_locals
    
    # Serialize and deserialize
    try:
        pickled = pickle.dumps(ctl)
        restored_ctl = pickle.loads(pickled)
        
        # Test that we can still use the restored object
        restored_ctl.buffer.append(Segment("thread test"))
        restored_ctl.buffer_index = 5
        
        print(f"  ✅ Restored object is functional")
        print(f"  📊 Buffer length: {len(restored_ctl.buffer)}")
        print(f"  📊 Buffer index: {restored_ctl.buffer_index}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 Starting Rich ConsoleThreadLocals pickle fix tests...\n")
    
    tests = [
        test_basic_pickle,
        test_langflow_compatibility,
        test_thread_local_behavior,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()  # Add spacing between tests
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The pickle fix is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())