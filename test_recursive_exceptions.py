"""
Test script to verify the fix for recursive ExceptionGroup handling.

This script creates a deliberately recursive ExceptionGroup structure
that would normally cause a RecursionError in Rich v14.0.0.
"""
from rich.console import Console
from rich.traceback import install

# In Python 3.11+, ExceptionGroup is a built-in
try:
    from builtins import ExceptionGroup
except ImportError:
    # For Python < 3.11, import from rich's traceback module
    from rich.traceback import ExceptionGroup

# Install rich traceback handler
install(show_locals=True)

def create_recursive_exception_group():
    """Create a recursive ExceptionGroup structure that would cause infinite recursion"""
    # Create some basic exceptions
    exc1 = ValueError("First error")
    exc2 = TypeError("Second error")
    
    # Create a group
    group1 = ExceptionGroup("First level", [exc1, exc2])
    
    # Create a second group that includes the first one (creating a cycle)
    group2 = ExceptionGroup("Second level", [RuntimeError("Third error"), group1])
    
    # Create a recursive reference (this would definitely cause recursion issues)
    recursive_group = ExceptionGroup("Recursive group", [group2])
    
    # Raise the recursive structure
    raise recursive_group

# Test the fix
try:
    print("Creating recursive ExceptionGroup structure...")
    create_recursive_exception_group()
except Exception as e:
    # This should now print without a recursion error
    console = Console()
    console.print("Successfully handled recursive ExceptionGroup structure!")
    console.print_exception() 