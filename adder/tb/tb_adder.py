import cocotb
from cocotb.triggers import Timer
async def test(dut, in1, in2, exp):
	dut.i_input1.value = in1
	dut.i_input2.value = in2
	await Timer(1, unit="ps")
	assert dut.o_output.value == exp, f"exxpected {exp} but got {dut.o_output.value}"

@cocotb.test()
async def tb_adder(dut):
	#initialise the signal 
	await test(dut, 0, 0, 0)
	await Timer(1, unit="ns")
	await test(dut, 0, 4, 4)
	await Timer(1, unit="ns")
	await test(dut, 4, 4, 8)
	await Timer(1, unit="ns")
	await test(dut, 8, 4, 12)



	for _ in range(2):
		await Timer(1, unit="ns")
