"""
Unit tests for ALU
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.alu import ALU


def test_alu_add():
    """Test ALU addition"""
    alu = ALU()
    result, zero = alu.execute(5, 3, ALU.ALU_ADD)
    assert result == 8, f"Expected 8, got {result}"
    assert not zero, "Zero flag should be False"
    print("✓ ALU ADD test passed")


def test_alu_sub():
    """Test ALU subtraction"""
    alu = ALU()
    result, zero = alu.execute(5, 3, ALU.ALU_SUB)
    assert result == 2, f"Expected 2, got {result}"
    assert not zero, "Zero flag should be False"
    
    result, zero = alu.execute(3, 3, ALU.ALU_SUB)
    assert result == 0, f"Expected 0, got {result}"
    assert zero, "Zero flag should be True"
    print("✓ ALU SUB test passed")


def test_alu_and():
    """Test ALU AND"""
    alu = ALU()
    result, zero = alu.execute(0b1100, 0b1010, ALU.ALU_AND)
    assert result == 0b1000, f"Expected {0b1000}, got {result}"
    print("✓ ALU AND test passed")


def test_alu_or():
    """Test ALU OR"""
    alu = ALU()
    result, zero = alu.execute(0b1100, 0b1010, ALU.ALU_OR)
    assert result == 0b1110, f"Expected {0b1110}, got {result}"
    print("✓ ALU OR test passed")


def test_alu_slt():
    """Test ALU set less than"""
    alu = ALU()
    result, zero = alu.execute(3, 5, ALU.ALU_SLT)
    assert result == 1, f"Expected 1, got {result}"
    
    result, zero = alu.execute(5, 3, ALU.ALU_SLT)
    assert result == 0, f"Expected 0, got {result}"
    print("✓ ALU SLT test passed")


if __name__ == "__main__":
    test_alu_add()
    test_alu_sub()
    test_alu_and()
    test_alu_or()
    test_alu_slt()
    print("\n✓ All ALU tests passed!")
