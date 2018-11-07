#!/usr/bin/python3
import subprocess
import sys
import html

def bytes_to_human(byte):
    if byte == 0:
        return "0b"
    res = ""
    unit = 0
    unitsList = ["B", "kiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
    while (byte > 0) and (unit < len(unitsList)-1):
        if res:
            res = " " + res
        res = "%d%s"%(byte%1024, unitsList[unit]) + res
        unit += 1
        byte = byte//1024
    return res

def main():
    command = "nm --demangle=gnu --print-size --format bsd -- " + " ".join(sys.argv[1:]) + "|c++filt -_"
    out = subprocess.check_output(["sh", "-c", command], universal_newlines=True)
    out = html.escape(out)


    print("var dataCodeSize = [")


    for line in out.splitlines():
        if not line:
            continue
        col = line.split(maxsplit=3);
        if (len(col) != 4) or (col[2] not in "wWtT"):
            continue

        print("    {")
        lenByte = int(col[1], base=16)
        print("""\
        "symbol": '%s',
        "size": "%d",
        "sizeHuman": "%s",
        """ % (col[3], lenByte, bytes_to_human(lenByte)))
        print("    },")


    print("""];""")



if __name__ == "__main__":
    main()
