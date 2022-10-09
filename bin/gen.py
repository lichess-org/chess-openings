#!/usr/bin/python3

import io
import re
import sys
from typing import Dict, List

try:
    import chess
    import chess.pgn
except ImportError:
    print("Need python-chess:", file=sys.stderr)
    print("$ pip3 install chess", file=sys.stderr)
    print(file=sys.stderr)
    raise


ECO_REGEX = re.compile(r"^[A-E]\d\d\Z")

INVALID_SPACE = re.compile(r"\s{2,}|^\s|\s\Z|\s,")


def err_printer(file_name: str, lno: int, err_msg: str, err_typ: str = "error") -> int:
    print(f"::{err_typ} file={file_name},line={lno}::{err_msg}", file=sys.stderr)
    return 1 if err_typ=="error" else 0


def main(arg, by_epd: Dict[str,List[str]], shortest_by_name:Dict[str,int]):
    ret = 0
    prev_eco = ""
    prev_name = ""

    with open(arg) as f:
        for lno, line in enumerate(f, 1):
            cols = line.rstrip("\n").split("\t")

            if len(cols) != 3:
                ret = err_printer(arg, lno, f"expected 3 columns, got {len(cols)}")
                continue

            if lno == 1:
                if cols != ["eco", "name", "pgn"]:
                    ret = err_printer(arg, lno, f"expected eco, name, pgn")
                continue

            eco, name, pgn = cols

            if not ECO_REGEX.match(eco):
                ret = err_printer(arg, lno, f"invalid eco")
                continue

            if INVALID_SPACE.search(name):
                ret = err_printer(arg, lno, f"invalid whitespace in name")
                continue

            try:
                board = chess.pgn.read_game(io.StringIO(pgn), Visitor=chess.pgn.BoardBuilder)
            except ValueError as err:
                ret = err_printer(arg, lno, f"{err}")
                continue

            if not board:
                ret = err_printer(arg, lno, f"Empty pgn")
                continue
            
            allowed_lowers = ["with","de","der","del","von","and"]
            if not all([word[0].isupper() for word in re.split(r"\s|-",name)\
            if word not in allowed_lowers and word.isalpha()]):
                err_printer(arg,lno,f"{name!r} word(s) beginning with lowercase letters", "warning")
            
            if shortest_by_name.get(name, -1) == len(board.move_stack):
                err_printer(arg, lno, f"{name!r} does not have a unique shortest line", "warning")
            try:
                shortest_by_name[name] = min(shortest_by_name[name], len(board.move_stack))
            except KeyError:
                shortest_by_name[name] = len(board.move_stack)

            clean_pgn = chess.Board().variation_san(board.move_stack)
            if clean_pgn != pgn:
                err_printer(arg, lno, f"unclean pgn: expected {clean_pgn!r}, got {pgn!r}")

            if name.count(":") > 1:
                err_printer(arg, lno, f"multiple ':' in name: {name}")

            for blacklisted in ["refused"]:
                if blacklisted in name.lower():
                    err_printer(arg, lno, f"blacklisted word ({blacklisted!r} in {name!r})", "warning")

            epd = board.epd()
            if epd in by_epd:
                err_printer(arg, lno, f"duplicate epd: {by_epd[epd]}")
            else:
                by_epd[epd] = cols

            if eco < prev_eco:
                err_printer(arg, lno, f"not ordered by eco ({eco} after {prev_eco})")
            elif (eco, name) < (prev_eco, prev_name):
                err_printer(arg, lno, f"not ordered by name ({name!r} after {prev_name!r})")
            prev_eco = eco
            prev_name = name

            print(eco, name, clean_pgn, " ".join(m.uci() for m in board.move_stack), epd, sep="\t")

    return ret


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print(f"Usage: {sys.argv[0]} *.tsv", file=sys.stderr)
        sys.exit(2)

    print("eco", "name", "pgn", "uci", "epd", sep="\t")

    by_epd: Dict[str,List[str]] = {}
    shortest_by_name: Dict[str,int] = {}
    ret = 0
    for arg in sys.argv[1:]:
        ret = max(ret, main(arg, by_epd, shortest_by_name))
    sys.exit(ret)
