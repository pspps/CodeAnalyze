#!/usr/bin/python3
import subprocess
import sys

def main():
    out = subprocess.check_output("nm --demangle --print-size --format posix --".split()+sys.argv[1:], universal_newlines=True)


    print("var dataCodeSize = [")


    for line in out.splitlines():
        if not line:
            continue
        col = line.split();
        if (len(col) != 4) or (col[1] not in "wWtT"):
            continue

        print("    {")
        print("""\
        "symbol": "%s",
        "size": "%d",
        """ % (col[0], int(col[3], base=16)))
        print("    },")


    print("""];""")



if __name__ == "__main__":
    main()
