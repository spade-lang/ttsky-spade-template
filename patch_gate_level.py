import yaml

with open("info.yaml") as f:
    yaml_content = yaml.safe_load(f)
    top_module = yaml_content["project"]["top_module"]

patch = f"""
    string __top_module;
    string __vcd_file;
    initial begin
        $value$plusargs("VCD_FILENAME=%s", __vcd_file);
        $dumpfile (__vcd_file);
        $dumpvars;
    end
"""

with open("test/gate_level_netlist.v") as f:
    content = f.read()

    # This makes the assumption that there is only one module in the post synthesis netlist
    patched = content.replace("input clk;", "input clk;\n" + patch)

    with open("test/patched.v", "w") as f:
        f.write(patched)
