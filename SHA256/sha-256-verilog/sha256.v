module sha256_chunk_loop (
    input clk, rst,
    input [255:0] hash_in,
    input [511:0] chunk_in,
    input chunk_flag,
    output [255:0] hash_out,
    output hash_out_valid
    );
    reg [6:0] round_cnt;
    reg [31:0] a_round, b_round, c_round, d_round, e_round, f_round, g_round, h_round;
    wire [31:0] a_temp, b_temp, c_temp, d_temp, e_temp, f_temp, g_temp, h_temp;
    wire [31:0] word_t2, word_t15, word_t2_ls1, word_t15_ls0, w_i, k_i;
    wire [31:0] a_in = hash_in[255:224], b_in = hash_in[223:192], c_in = hash_in[191:160], d_in = hash_in[159:128];
    wire [31:0] e_in = hash_in[127:96], f_in = hash_in[95:64], g_in = hash_in[63:32], h_in = hash_in[31:0];
    
    assign hash_out = {
        a_in + a_round, b_in + b_round, c_in + c_round, d_in + d_round, e_in + e_round, f_in + f_round, g_in + g_round, h_in + h_round
    };
    assign hash_out_valid = (round_cnt == 64); // 64 rounds

    always @(posedge clk)
    begin
        if (chunk_flag) begin 
            a_round <= a_in; b_round <= b_in; c_round <= c_in; d_round <= d_in;
            e_round <= e_in; f_round <= f_in; g_round <= g_in; h_round <= h_in;
            round_cnt <= 0;
        end else begin 
            a_round <= a_temp; b_round <= b_temp; c_round <= c_temp; d_round <= d_temp;
            e_round <= e_temp; f_round <= f_temp; g_round <= g_temp; h_round <= h_temp;
            round_cnt <= round_cnt + 1;
        end
    end

    sha256_round sha256_round (
        .k_i(k_i), .w_i(w_i),
        .a_in(a_round), .b_in(b_round), .c_in(c_round), .d_in(d_round),
        .e_in(e_round), .f_in(f_round), .g_in(g_round), .h_in(h_round),
        .a_out(a_temp), .b_out(b_temp), .c_out(c_temp), .d_out(d_temp),
        .e_out(e_temp), .f_out(f_temp), .g_out(g_temp), .h_out(h_temp)
    );

    lcase_sigma0 #(.WORDSIZE(32)) lcase_sigma0_inst (.ls0_in(word_t15), .ls0_out(word_t15_ls0));
    lcase_sigma1 #(.WORDSIZE(32)) lcase_sigma1_inst (.ls1_in(word_t2), .ls1_out(word_t2_ls1));

    word_generator #(.WORDSIZE(32)) word_generator_inst (
        .clk(clk),
        .chunk(chunk_in), .chunk_flag(chunk_flag),
        .word_t2_ls1(word_t2_ls1), .word_t15_ls0(word_t15_ls0),
        .word_t2(word_t2), .word_t15(word_t15),
        .word_out(w_i)
    );

    lookup_k_constants lookup_k_constants_inst (
        .round_cnt(round_cnt), .k_i(k_i)
    );
endmodule


module sha256_round #(parameter WORDSIZE=32) (
    input [31:0] k_i, w_i,
    input [31:0] a_in, b_in, c_in, d_in, e_in, f_in, g_in, h_in,
    output [31:0] a_out, b_out, c_out, d_out, e_out, f_out, g_out, h_out
    );
    wire [31:0] ch_e_f_g, maj_a_b_c, us0_a, us1_e;

    choice #(.WORDSIZE(32)) choice_inst (
        .ch_in_x(e_in), .ch_in_y(f_in), .ch_in_z(g_in), .ch_out(ch_e_f_g)
    );

    majority #(.WORDSIZE(32)) majority_inst (
        .maj_in_x(a_in), .maj_in_y(b_in), .maj_in_z(c_in), .maj_out(maj_a_b_c)
    );

    ucase_sigma0 #(.WORDSIZE(32)) us0_inst (
        .us0_in(a_in), .us0_out(us0_a)
    );

    ucase_sigma1 #(.WORDSIZE(32)) us1_inst (
        .us1_in(e_in), .us1_out(us1_e)
    );

    wire [WORDSIZE-1:0] temp1 = h_in + us1_e + ch_e_f_g + k_i + w_i;
    wire [WORDSIZE-1:0] temp2 = us0_a + maj_a_b_c;

    assign a_out = temp1 + temp2;
    assign b_out = a_in;
    assign c_out = b_in;
    assign d_out = c_in;
    assign e_out = d_in + temp1;
    assign f_out = e_in;
    assign g_out = f_in;
    assign h_out = g_in;
endmodule

//ucase_sigma0: upper case sigma0
module ucase_sigma0 #(parameter WORDSIZE=32) (
    input wire [WORDSIZE-1:0] us0_in,
    output wire [WORDSIZE-1:0] us0_out
    );
    assign us0_out = ({us0_in[1:0], us0_in[31:2]} ^ {us0_in[12:0], us0_in[31:13]} ^ {us0_in[21:0], us0_in[31:22]});
endmodule


//ucase_sigma1: upper case sigma1
module ucase_sigma1 #(parameter WORDSIZE=32) (
    input wire [WORDSIZE-1:0] us1_in,
    output wire [WORDSIZE-1:0] us1_out
    );
    assign us1_out = ({us1_in[5:0], us1_in[31:6]} ^ {us1_in[10:0], us1_in[31:11]} ^ {us1_in[24:0], us1_in[31:25]});
endmodule


//lcase_sigma0: lower case sigma0
module lcase_sigma0 #(parameter WORDSIZE=32) (
    input wire [WORDSIZE-1:0] ls0_in,
    output wire [WORDSIZE-1:0] ls0_out
    );
    assign ls0_out = ({ls0_in[6:0], ls0_in[31:7]} ^ {ls0_in[17:0], ls0_in[31:18]} ^ (ls0_in >> 3));
endmodule


//lcase_sigma1: lower case sigma1
module lcase_sigma1 #(parameter WORDSIZE=32) (
    input wire [WORDSIZE-1:0] ls1_in,
    output wire [WORDSIZE-1:0] ls1_out
    );
    assign ls1_out = ({ls1_in[16:0], ls1_in[31:17]} ^ {ls1_in[18:0], ls1_in[31:19]} ^ (ls1_in >> 10));
endmodule


module lookup_k_constants (
	input [6:0] round_cnt,
	output [31:0] k_i
    );
	reg [31:0] k_i_cur;
	assign k_i = k_i_cur;

	always @*
		begin : round_mux
			case(round_cnt)
                00: k_i_cur = 32'h428a2f98;
                01: k_i_cur = 32'h71374491;
                02: k_i_cur = 32'hb5c0fbcf;
                03: k_i_cur = 32'he9b5dba5;
                04: k_i_cur = 32'h3956c25b;
                05: k_i_cur = 32'h59f111f1;
                06: k_i_cur = 32'h923f82a4;
                07: k_i_cur = 32'hab1c5ed5;
                08: k_i_cur = 32'hd807aa98;
                09: k_i_cur = 32'h12835b01;
                10: k_i_cur = 32'h243185be;
                11: k_i_cur = 32'h550c7dc3;
                12: k_i_cur = 32'h72be5d74;
                13: k_i_cur = 32'h80deb1fe;
                14: k_i_cur = 32'h9bdc06a7;
                15: k_i_cur = 32'hc19bf174;
                16: k_i_cur = 32'he49b69c1;
                17: k_i_cur = 32'hefbe4786;
                18: k_i_cur = 32'h0fc19dc6;
                19: k_i_cur = 32'h240ca1cc;
                20: k_i_cur = 32'h2de92c6f;
                21: k_i_cur = 32'h4a7484aa;
                22: k_i_cur = 32'h5cb0a9dc;
                23: k_i_cur = 32'h76f988da;
                24: k_i_cur = 32'h983e5152;
                25: k_i_cur = 32'ha831c66d;
                26: k_i_cur = 32'hb00327c8;
                27: k_i_cur = 32'hbf597fc7;
                28: k_i_cur = 32'hc6e00bf3;
                29: k_i_cur = 32'hd5a79147;
                30: k_i_cur = 32'h06ca6351;
                31: k_i_cur = 32'h14292967;
                32: k_i_cur = 32'h27b70a85;
                33: k_i_cur = 32'h2e1b2138;
                34: k_i_cur = 32'h4d2c6dfc;
                35: k_i_cur = 32'h53380d13;
                36: k_i_cur = 32'h650a7354;
                37: k_i_cur = 32'h766a0abb;
                38: k_i_cur = 32'h81c2c92e;
                39: k_i_cur = 32'h92722c85;
                40: k_i_cur = 32'ha2bfe8a1;
                41: k_i_cur = 32'ha81a664b;
                42: k_i_cur = 32'hc24b8b70;
                43: k_i_cur = 32'hc76c51a3;
                44: k_i_cur = 32'hd192e819;
                45: k_i_cur = 32'hd6990624;
                46: k_i_cur = 32'hf40e3585;
                47: k_i_cur = 32'h106aa070;
                48: k_i_cur = 32'h19a4c116;
                49: k_i_cur = 32'h1e376c08;
                50: k_i_cur = 32'h2748774c;
                51: k_i_cur = 32'h34b0bcb5;
                52: k_i_cur = 32'h391c0cb3;
                53: k_i_cur = 32'h4ed8aa4a;
                54: k_i_cur = 32'h5b9cca4f;
                55: k_i_cur = 32'h682e6ff3;
                56: k_i_cur = 32'h748f82ee;
                57: k_i_cur = 32'h78a5636f;
                58: k_i_cur = 32'h84c87814;
                59: k_i_cur = 32'h8cc70208;
                60: k_i_cur = 32'h90befffa;
                61: k_i_cur = 32'ha4506ceb;
                62: k_i_cur = 32'hbef9a3f7;
                63: k_i_cur = 32'hc67178f2;
			endcase
		end
endmodule 


module sha256_hash_ini(
    output [255:0] hash_0
    );
    assign hash_0 = {
        32'h6A09E667, 32'hBB67AE85, 32'h3C6EF372, 32'hA54FF53A,
        32'h510E527F, 32'h9B05688C, 32'h1F83D9AB, 32'h5BE0CD19
    };
endmodule


module choice #(parameter WORDSIZE=32) (
    input wire [WORDSIZE-1:0] ch_in_x, ch_in_y, ch_in_z,
    output wire [WORDSIZE-1:0] ch_out
    );
    assign ch_out = ((ch_in_x & ch_in_y) ^ (~ch_in_x & ch_in_z));
endmodule


module majority #(parameter WORDSIZE=32) (
    input wire [WORDSIZE-1:0] maj_in_x, maj_in_y, maj_in_z,
    output wire [WORDSIZE-1:0] maj_out
    );
    assign maj_out = (maj_in_x & maj_in_y) ^ (maj_in_x & maj_in_z) ^ (maj_in_y & maj_in_z);
endmodule


module word_generator #(parameter WORDSIZE=32) (
    input clk,
    input [WORDSIZE*16-1:0] chunk,
    input chunk_flag,
    input [WORDSIZE-1:0] word_t2_ls1, word_t15_ls0,
    output [WORDSIZE-1:0] word_t2, word_t15,
    output [WORDSIZE-1:0] word_out
    );
    reg [WORDSIZE*16-1:0] word_array_cur;
    assign word_t2 = word_array_cur[WORDSIZE*2-1:WORDSIZE*1];
    assign word_t15 = word_array_cur[WORDSIZE*15-1:WORDSIZE*14];
    wire [WORDSIZE-1:0] word_t7 = word_array_cur[WORDSIZE*7-1:WORDSIZE*6];
    wire [WORDSIZE-1:0] word_t16 = word_array_cur[WORDSIZE*16-1:WORDSIZE*15];

    wire [WORDSIZE-1:0] word_next = word_t2_ls1 + word_t7 + word_t15_ls0 + word_t16;
    wire [WORDSIZE*16-1:0] word_array_temp = {word_array_cur[WORDSIZE*15-1:0], word_next};
    assign word_out = word_array_cur[WORDSIZE*16-1:WORDSIZE*15];

    always @(posedge clk)
    begin
        if (chunk_flag) begin // The first 16
            word_array_cur <= chunk;
        end else begin 
            word_array_cur <= word_array_temp; //The remaining 48
        end
    end
endmodule