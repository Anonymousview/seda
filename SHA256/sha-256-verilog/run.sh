echo "Running the script >>>"

echo "1.Compiling the verilog code: "
iverilog -o ./out/sha256 sha256.v tb_sha256.v

echo "2.Running the executable: "
vvp ./out/sha256

echo "3.Generating the wave form: "
gtkwave ./out/vcd_sha256.vcd
