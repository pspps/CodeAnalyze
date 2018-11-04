#!/usr/bin/python3
import os
import sys

def get_deps(filename):
    with open(filename, "r") as f:
        data = f.read()
    data = data.replace("\\\n",  " ")

    for i in data.split("\n"):
        if not i:
            continue
        split = i.strip().split(":", 1)
        target = split[0]
        deps = set(split[1].split())
        yield (target, deps)

def main():
    includes = {}
    if len(sys.argv) == 1:
        paths = ["."]
    else:
        paths = sys.argv[1:]

    for path in paths:
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.endswith(".d"):
                    path = "%s/%s"%(root, name)
                    for target, deps in get_deps(path):
                        if not deps:
                            continue
                        if target not in includes:
                            includes[target] = set()
                        includes[target] |= deps

    included = {}
    for key, values in includes.items():
        for value in values:
            if value not in included:
                included[value] = set()
            included[value].add(key)



    print("var dataInclude = [")
    for key, values in includes.items():
        print("    {")
        print("""\
        "obj": "%s",
        "depsLen": "%d",
        "deps": "%s"
        """ % (key, len(values), "<br>".join(values)))
        print("    },")
    print("""];""")


    print("var dataIncluded = [")
    for key, values in included.items():
        print("    {")
        print("""\
        "header": "%s",
        "objsLen": "%d",
        "objs": "%s"
        """ % (key, len(values), "<br>".join(values)))
        print("    },")
    print("""];""")



if __name__ == "__main__":
    main()
