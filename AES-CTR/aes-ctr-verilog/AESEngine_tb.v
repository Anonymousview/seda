module AESEngine_tb;
    reg [127:0] data_in_128;
    wire [127:0] data_out_128;
    reg [127:0] key_128;

    reg [127:0] data_in_192;
    wire [127:0] data_out_192;
    reg [191:0] key_192;

    reg [127:0] data_in_256;
    wire [127:0] data_out_256;
    reg [255:0] key_256;

    AESEngine aes_128 (
        .data_in(data_in_128),
        .key(key_128),
        .data_out(data_out_128)
    );

    AESEngine #(192, 12, 6) aes_192 (
        .data_in(data_in_192),
        .key(key_192),
        .data_out(data_out_192)
    );

    AESEngine #(256, 14, 8) aes_256 (
        .data_in(data_in_256),
        .key(key_256),
        .data_out(data_out_256)
    );

    initial begin
        $dumpfile("./vcd_aes_engine.vcd");
        $dumpvars;

        $monitor("\ndata_in_128 = %h\nkey_128 = %h\ndata_out_128 = %h",data_in_128, key_128, data_out_128);
        data_in_128=128'h00000000000000000000000000000001;
        key_128=128'h00000000000000000000000000000001;
        #10;

        $monitor("\ndata_in_192 = %h\nkey_192 = %h\ndata_out_192= %h",data_in_192, key_192, data_out_192);
        data_in_192=128'h1234567890abcdef1234567890abcdef;
        key_192=196'h1234567890abcdef1234567890abcdef1234567890abcdef;
        #10;

        $monitor("\ndata_in_256 = %h\nkey_256 = %h\ndata_out_256 = %h",data_in_256,key_256,data_out_256);
        data_in_256=128'habcdef1234567890abcdef1234567890;
        key_256=256'habcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890;
        #10;
    end
endmodule