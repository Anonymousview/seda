echo "Running the script >>>"

echo "1.Compiling the verilog code: "
iverilog -o ./exe_aes_engine AESEngine_tb.v AESEngine.v

echo "2.Running the executable: "
vvp ./exe_aes_engine

echo "3.Generating the wave form: "
gtkwave ./vcd_aes_engine.vcd
