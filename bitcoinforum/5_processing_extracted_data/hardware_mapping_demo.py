mapping0 = {
    "\"&\"-\" screw terminals": "unknown",
    "\"oc dual-x\"": "unknown",
    "#1 computer": "unknown",
    "#11": "unknown",
    "#12 2-conductor with ground wire cable": "unknown",
    "#13": "unknown",
    "#2": "unknown",
    "#2 computer": "unknown",
    "#2 philips bit": "unknown",
    "#6/#8": "unknown",
    "#8-32 hex nut": "unknown",
    "#8-32 x 1-1/4\" machine screws": "unknown",
    "$1.1k ups/battery bank combo": "unknown",
    "$150 laptop": "unknown",
    "$16 holmes personal fans": "unknown",
    "$1600 laptop": "unknown",
    "$200 item from china": "unknown",
    "$200 laptops": "unknown",
    "$25 fans": "unknown",
    "$400 gpus": "unknown",
    "$400 rig": "unknown",
    "$5 evercool single fan": "unknown",
    "$500 pc": "unknown",
    "(+5v)": "unknown",
    "* .batstart batch:cgminer.exe": "unknown",
    "+ track": "unknown",
    "-framework opencl": "unknown",
    "-l/opt/local/lib": "unknown",
    "-lcurl": "unknown",
    "-ldl": "unknown",
    "-lm lib/libgnu.a": "unknown",
    "-lncurses": "unknown",
    "-lpthread": "unknown",
    "-qt client": "unknown",
    "-v -w256 -f0": "unknown",
    ".333 ghs sticks": "unknown",
    ".336 asicminers": "unknown",
    ".bat file": "unknown",
    ".bat or .cmd files": "unknown",
    ".net": "unknown",
    ".net 3.5 framework": "unknown",
    ".net 4 framework": "unknown",
    ".net framework": "unknown",
    ".net framework v4.0": "unknown",
    ".net program widget thingie": "unknown",
    ".vbs script": "unknown",
    "/dev/ati/card0": "unknown",
    "/dev/ati/card1": "unknown",
    "/dev/sda1": "unknown",
    "/dev/sdx": "unknown",# All entries in the provided collection do not correspond to any known mining hardware from the list.
}


def map_hardware_to_table(string):
    res = "not found"
    for i in range(0, 488):
        if string in globals()["mapping" + str(i)]:
            res = globals()["mapping" + str(i)][string]
            break
    return res