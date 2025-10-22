"""
Integration test for MIPS pipeline with simple programs
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.processor import MIPSPipeline
from src.asm_utils import *


def test_simple_arithmetic():
    """Test simple arithmetic operations"""
    print("\n=== Test: Simple Arithmetic ===")
    
    processor = MIPSPipeline()
    
    # Program: Add two numbers
    # $t0 = 5, $t1 = 3, $t2 = $t0 + $t1
    program = [
        addi(REGISTERS['t0'], REGISTERS['zero'], 5),   # $t0 = 5
        addi(REGISTERS['t1'], REGISTERS['zero'], 3),   # $t1 = 3
        add(REGISTERS['t2'], REGISTERS['t0'], REGISTERS['t1']),  # $t2 = $t0 + $t1
        nop(),
        nop(),
        nop(),
        nop()
    ]
    
    processor.load_program(program)
    processor.run(max_cycles=20, verbose=False)
    
    regs = processor.get_register_state()
    assert regs[REGISTERS['t0']] == 5, "t0 should be 5"
    assert regs[REGISTERS['t1']] == 3, "t1 should be 3"
    assert regs[REGISTERS['t2']] == 8, "t2 should be 8"
    
    print(f"✓ Arithmetic test passed")
    print(f"  $t0 = {regs[REGISTERS['t0']]}")
    print(f"  $t1 = {regs[REGISTERS['t1']]}")
    print(f"  $t2 = {regs[REGISTERS['t2']]}")
    
    stats = processor.get_statistics()
    print(f"  Cycles: {stats['cycles']}, Instructions: {stats['instructions']}, CPI: {stats['cpi']:.2f}")


def test_load_store():
    """Test load and store operations"""
    print("\n=== Test: Load/Store ===")
    
    processor = MIPSPipeline()
    
    # Pre-load data into memory
    processor.data_mem.write(0, 42)
    processor.data_mem.write(4, 100)
    
    # Program: Load from memory, modify, store back
    program = [
        lw(REGISTERS['t0'], 0, REGISTERS['zero']),     # $t0 = Memory[0] = 42
        addi(REGISTERS['t1'], REGISTERS['t0'], 10),    # $t1 = $t0 + 10 = 52
        sw(REGISTERS['t1'], 8, REGISTERS['zero']),     # Memory[8] = $t1 = 52
        nop(),
        nop(),
        nop(),
        nop()
    ]
    
    processor.load_program(program)
    processor.run(max_cycles=20, verbose=False)
    
    regs = processor.get_register_state()
    assert regs[REGISTERS['t0']] == 42, "t0 should be 42"
    assert regs[REGISTERS['t1']] == 52, "t1 should be 52"
    assert processor.data_mem.read(8) == 52, "Memory[8] should be 52"
    
    print(f"✓ Load/Store test passed")
    print(f"  $t0 = {regs[REGISTERS['t0']]}")
    print(f"  $t1 = {regs[REGISTERS['t1']]}")
    print(f"  Memory[8] = {processor.data_mem.read(8)}")
    
    stats = processor.get_statistics()
    print(f"  Cycles: {stats['cycles']}, Instructions: {stats['instructions']}, CPI: {stats['cpi']:.2f}")


def test_branch():
    """Test branch instructions"""
    print("\n=== Test: Branch ===")
    
    processor = MIPSPipeline()
    
    # Program with branch
    program = [
        addi(REGISTERS['t0'], REGISTERS['zero'], 5),   # $t0 = 5
        addi(REGISTERS['t1'], REGISTERS['zero'], 5),   # $t1 = 5
        beq(REGISTERS['t0'], REGISTERS['t1'], 2),      # if $t0 == $t1, skip 2 instructions
        addi(REGISTERS['t2'], REGISTERS['zero'], 99),  # (skipped) $t2 = 99
        addi(REGISTERS['t3'], REGISTERS['zero'], 88),  # (skipped) $t3 = 88
        addi(REGISTERS['t4'], REGISTERS['zero'], 77),  # $t4 = 77
        nop(),
        nop(),
        nop()
    ]
    
    processor.load_program(program)
    processor.run(max_cycles=20, verbose=False)
    
    regs = processor.get_register_state()
    assert regs[REGISTERS['t0']] == 5, "t0 should be 5"
    assert regs[REGISTERS['t1']] == 5, "t1 should be 5"
    assert regs[REGISTERS['t2']] == 0, "t2 should be 0 (skipped)"
    assert regs[REGISTERS['t3']] == 0, "t3 should be 0 (skipped)"
    assert regs[REGISTERS['t4']] == 77, "t4 should be 77"
    
    print(f"✓ Branch test passed")
    print(f"  $t0 = {regs[REGISTERS['t0']]}")
    print(f"  $t1 = {regs[REGISTERS['t1']]}")
    print(f"  $t2 = {regs[REGISTERS['t2']]} (skipped)")
    print(f"  $t4 = {regs[REGISTERS['t4']]}")
    
    stats = processor.get_statistics()
    print(f"  Cycles: {stats['cycles']}, Instructions: {stats['instructions']}, CPI: {stats['cpi']:.2f}")


def test_data_hazard_with_forwarding():
    """Test data hazard resolution with forwarding"""
    print("\n=== Test: Data Hazard with Forwarding ===")
    
    processor = MIPSPipeline()
    
    # Program with data dependencies (requires forwarding)
    program = [
        addi(REGISTERS['t0'], REGISTERS['zero'], 10),   # $t0 = 10
        addi(REGISTERS['t1'], REGISTERS['t0'], 5),      # $t1 = $t0 + 5 = 15 (depends on t0)
        add(REGISTERS['t2'], REGISTERS['t1'], REGISTERS['t0']),  # $t2 = $t1 + $t0 = 25 (depends on t1)
        nop(),
        nop(),
        nop()
    ]
    
    processor.load_program(program)
    processor.run(max_cycles=20, verbose=False)
    
    regs = processor.get_register_state()
    assert regs[REGISTERS['t0']] == 10, "t0 should be 10"
    assert regs[REGISTERS['t1']] == 15, "t1 should be 15"
    assert regs[REGISTERS['t2']] == 25, "t2 should be 25"
    
    print(f"✓ Forwarding test passed")
    print(f"  $t0 = {regs[REGISTERS['t0']]}")
    print(f"  $t1 = {regs[REGISTERS['t1']]}")
    print(f"  $t2 = {regs[REGISTERS['t2']]}")
    
    stats = processor.get_statistics()
    print(f"  Cycles: {stats['cycles']}, Instructions: {stats['instructions']}, CPI: {stats['cpi']:.2f}")


if __name__ == "__main__":
    test_simple_arithmetic()
    test_load_store()
    test_branch()
    test_data_hazard_with_forwarding()
    print("\n✓ All integration tests passed!")
