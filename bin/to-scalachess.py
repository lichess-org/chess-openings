#!/usr/bin/python3

import sys
import itertools


def main(argv):
    name = "X"
    for prefix in "abcde":
        if f"{prefix}.tsv" in argv[1]:
            name = prefix.upper()

    print("package chess")
    print("package opening")
    print()
    print("// Generated from https://github.com/niklasf/eco")
    print("// format: off")
    print(f"private[opening] object FullOpeningPart{name} {{")
    print()
    print("  def db: Vector[FullOpening] = Vector(")

    for line in itertools.islice(open(argv[1]), 1, None):
        cols = line.split("\t")
        print(f"""new FullOpening("{cols[0]}", "{cols[1]}", "{cols[2]}"),""")

    print("  )")
    print("}")


if __name__ == "__main__":
    main(sys.argv)
