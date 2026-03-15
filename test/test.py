# top = tt_um_example

import cocotb
from spade import SpadeExt
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge


# Smoke test for the whole project. Since it is called _gatelevel it will be tested
# both pre- and post synthesis.
@cocotb.test()
async def test_project_gatelevel(dut):
    # Set up the Spade integration and start a clock
    s = SpadeExt(dut)

    clk = dut.clk
    await cocotb.start(Clock(clk, period=10, units='ns').start())

    # Avoid issues on the first clock edge by waiting one clock cycle
    await FallingEdge(clk)

    # Since this is a gate level test, we have to set VGND and VPWR if those exist
    if hasattr(dut, "VGND"):
        dut.VGND = 0
        dut.VPWR = 1

    # Initial input values
    s.i.ui_in = "[false, false, false, false,  false, false, false, false]"
    # Enabble needs to be set for simulation to not be all X
    s.i.ena = True

    # Reset. For a few cycles to let the synchronizers settle
    s.i.rst_n = False
    [await FallingEdge(clk) for _ in range(0, 10)]
    s.i.rst_n = True
    await FallingEdge(clk)


    # Start of actual tests

    # Without input, we expect the input to be 0
    for _ in range(0, 5):
        s.i.uo_out.assert_eq("&0")
        await FallingEdge(clk)

    # Turn on up
    s.i.ui_in = "[true, false, false, false,  false, false, false, false]"

    # Wait for the synchronization
    for _ in range(0, 3):
        await FallingEdge(clk)

    # Since we check for rising edge, we expect the output to be 1 until something changes
    for _ in range(0, 5):
        s.i.uo_out.assert_eq("&1")
        await FallingEdge(clk)

    # Without another input, we expect the value to still remain
    s.i.ui_in = "[false, false, false, false,  false, false, false, false]"
    for _ in range(0, 5):
        s.i.uo_out.assert_eq("&1")
        await FallingEdge(clk)

    # And so on...
    

