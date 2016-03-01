`timescale 1ns / 100ps

module lab1_tbw;
    reg clk;

    wire out;

    initial begin
        // Initialize inputs
        clk <= 0;

        // Wait 100 ns for global reset to finish
        #100;

        forever
            clk = #10 ~clk;
    end

endmodule

