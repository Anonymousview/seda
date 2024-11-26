// Online testing: https://sha256algorithm.com/
module tb_sha256;
  reg chunk_ready = 0;
  wire chunk_end;
  wire [255:0] hash_0_in, digest_out;
  sha256_hash_ini sha256_hash_ini_inst (.hash_0(hash_0_in));
  sha256_chunk_loop sha256_chunk_loop_inst (
      .clk(clk), .rst(rst),
      .hash_in(hash_0_in), .chunk_in(digest_in),
      .chunk_flag(chunk_ready),
      .hash_out(digest_out),
      .hash_out_valid(chunk_end) 
  );

  // One pre-processed 512-bit digest_in of data:
  // STEP-1: padding bits. a=61,b=62,c=63, padding="1"+423"0" 
  // STEP-2: adding length. abc=3 chars=24 bits=18(hex)
  wire [511:0] digest_in = {
    512'h61626380000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000018  
  };

  reg [31:0] ticks = 0; 
  reg clk = 1'b0;
  reg rst = 1'b0;

  initial begin
    $dumpfile("./out/vcd_sha256.vcd");
    $dumpvars;

    $display("\n******************************* START *******************************\n");
    $display("INPUT: %h", digest_in);
    #1;
    clk = 1;
    #1;
    clk = 0;

    chunk_ready = 1'b1;
    #1;
    clk = 1;
    #1;
    clk = 0;

    chunk_ready = 1'b0;
    repeat (100) begin
      #1;
      clk = 1;
      #1;
      clk = 0;
      if (chunk_end) begin
        $display("OUTPUT: %h", digest_out);
      end
    end
    $display("\n******************************** END ********************************\n");
    $finish;
  end
endmodule