"""
Unit tests for Register File
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.register_file import RegisterFile


def test_register_read_write():
    """Test basic register read/write"""
    rf = RegisterFile()
    
    # Write to register 5
    rf.write(5, 100)
    assert rf.read(5) == 100, "Failed to write/read register 5"
    
    # Write to register 10
    rf.write(10, -50)
    assert rf.read(10) == -50, "Failed to write/read register 10"
    
    print("✓ Register read/write test passed")


def test_register_zero():
    """Test that register 0 is always 0"""
    rf = RegisterFile()
    
    # Try to write to register 0
    rf.write(0, 100)
    assert rf.read(0) == 0, "Register 0 should always be 0"
    
    print("✓ Register $0 test passed")


def test_register_bounds():
    """Test register bounds"""
    rf = RegisterFile()
    
    # Test all valid registers
    for i in range(1, 32):
        rf.write(i, i * 10)
        assert rf.read(i) == i * 10, f"Failed on register {i}"
    
    print("✓ Register bounds test passed")


if __name__ == "__main__":
    test_register_read_write()
    test_register_zero()
    test_register_bounds()
    print("\n✓ All Register File tests passed!")
