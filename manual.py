import sys
import json
import collections
import chess
import pyperclip
import time

out = open(sys.argv[2], "x")

def p(m):
    board = chess.Board()

    if m.startswith("."):
        m = "1" + m

    for token in m.replace(".", ". ").replace("D", "Q").replace("S", "N").replace("L", "B").replace("T", "R").strip().split():
        if token[0].isdigit():
            continue

        try:
            board.push_uci(token)
        except ValueError:
            board.push_san(token)

    return board

def m(board):
    switchyard = collections.deque()
    while board.move_stack:
        switchyard.append(board.pop())

    builder = []
    while switchyard:
        move = switchyard.pop()
        builder.append(board.uci(move))
        board.push(move)

    return " ".join(builder)

def f(board):
    fen = []
    fen.append(board.board_fen())
    fen.append("w" if board.turn == chess.WHITE else "b")
    fen.append(board.castling_xfen())
    return " ".join(fen)

def fast_input():
    print("Waiting for clipboard ...")
    old = pyperclip.paste()
    while old == pyperclip.paste():
        time.sleep(1)
        print("Still waiting ...")

    return pyperclip.paste()

done = False

for line in open(sys.argv[1]):
    record = json.loads(line)
    print("---")
    print(line.strip())
    print(record["id"])
    print(record["f"] + " - 0 1")
    print(record["n"])
    pyperclip.copy(record["n"])
    print("\a")
    print(record["m"])
    if record["m"] is None:
        input("CONFIRM")
        record["m"] = ""

    board = chess.Board(record["f"] + " - 0 1")

    try:
        if record["m"] != "XXX":
            f(p(record["m"]))
    except ValueError as err:
        print("\a")
        time.sleep(0.5)
        print("\a")
        time.sleep(0.5)
        print("\a")
        time.sleep(0.5)
        print("\a")
        print(" >>>>>================ BOINg =========== <<<<<<<<<<<<")
        print(err)
        record["m"] = "XXX"

    while not done and (record["m"] == "XXX" or f(p(record["m"])) != f(board)):
        #if record["m"] == "XXX":
        #    break

        print(board)
        print()
        if record["m"] != "XXX":
            print(p(record["m"]))

        i = fast_input()

        if i.strip() == "DONE":
            done = True
            break

        if i.strip() == "XXX":
            record["m"] = "XXX"
            break
        else:
            try:
                record["m"] = m(p(i))
            except ValueError as ex:
                print(ex)
                print("\a")
                time.sleep(0.5)
                print("\a")
                time.sleep(0.5)
                print("\a")
                time.sleep(0.5)
                print("\a")

    print(json.dumps(record, sort_keys=True))
    print(json.dumps(record, sort_keys=True), file=out, flush=True)
