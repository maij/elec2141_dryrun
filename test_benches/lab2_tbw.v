`timescale 1ns / 100ps

/*
 * Lab 2 test bench - Vote circuit
 */

module lab2_tbw;
    // Local variables
    reg clk;     // Clock signal for incrementing inputs (10 MHz)
    reg reset;   // Active-high reset

    // Inputs
    reg Z;
    reg X;
    reg Y;
    reg W;

    // Output
    wire P;

    Votecircuit UUT (
        .Z(Z),
        .X(X),
        .Y(Y),
        .W(W),
        .P(P)
    );
    initial begin
        $display("Beginning simulation of lab2");
        $display(" Z | Y | X | W || P ||");
    end

    initial begin
        Z     <= 1'b0;
        Y     <= 1'b0;
        X     <= 1'b0;
        W     <= 1'b0;
        clk   <= 1'b0;
        // Reset for 100ns
        reset <= 1'b1;
        #100;

        // Come out of reset
        reset <= 1'b0;

        // Set maximum execution time of this test bench to 5ns
        #5000;
        $finish;
    end


    always @(posedge clk) begin
        if (~reset) begin
            $display(" %b | %b | %b | %b || %b ||", Z, Y, X, W, P);
            //$display("%4b : %b", {Z, Y, X, W}, P); 
            {Z, Y, X, W} <= {Z, Y, X, W} + 1;
        end
    end

    initial forever
        clk <= #50 ~clk;

endmodule

