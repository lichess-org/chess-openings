#!/usr/bin/python3

import chess.pgn
import sys
import io
import itertools


def main(argv):
    name = "X"
    for prefix in "abcde":
        if f"{prefix}.tsv" in argv[1]:
            name = prefix.upper()

    print("package chess")
    print("package opening")
    print()
    print("// Generated from https://github.com/lichess-org/chess-openings")
    print("// format: off")
    print(f"private[opening] object FullOpeningPart{name} {{")
    print()
    print("  def db: Vector[FullOpening] = Vector(")

    for line in itertools.islice(open(argv[1]), 1, None):
        eco, name, pgn, uci, _ = line.split("\t")
        board = chess.pgn.read_game(io.StringIO(pgn), Visitor=chess.pgn.BoardBuilder)
        print(f"""new FullOpening("{eco}", "{name}", "{board.epd()}", "{uci}", "{pgn}"),""")

    print("  )")
    print("}")


if __name__ == "__main__":
    main(sys.argv)
