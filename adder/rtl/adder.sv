`timescale 1ns / 1ps

module adder(i_input1,
             i_input2,
             o_output);

parameter WIDTH = 32;

input logic [WIDTH-1 : 0] i_input1;
input logic [WIDTH-1 : 0] i_input2;

output logic [WIDTH-1 : 0] o_output;

always_comb begin 
    o_output = i_input1 + i_input2;
end

endmodule