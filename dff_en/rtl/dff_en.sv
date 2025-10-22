`timescale 1ns / 1ps
module dff_en(i_clk,
	   i_reset,
	   i_en,
	   i_input,
	   o_output);

parameter WIDTH = 64;

input i_clk;
input i_reset;
input i_en;
input [WIDTH-1:0] i_input;

output reg [WIDTH-1:0] o_output;

always_ff @ (posedge i_clk) begin
   if (i_reset) begin
	o_output <= 'b0;
   end else begin
	if (i_en) 
	    o_output <= i_input;
   end
end

endmodule
   
