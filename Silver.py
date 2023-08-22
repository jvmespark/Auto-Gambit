
import chess_engine as engine
import argparse
import core

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    gamestate = engine.gamestate()

    parser.add_argument('--play',
                    default=["cmd"],
                    help='Play on cmd[default] or gui\n\n',
                    type=str,
                    nargs=1
                    )
    parser.add_argument('--computer',
                    default=["disabled"],
                    help='Choose which method to utilize the computer AI\nOptions:\ndisabled[default]\nagainst: Play against the algorithm\nautoplay: Have the engine play against itself\n\n',
                    type=str,
                    nargs=1
                    )
    parser.add_argument('--algo',
                    default=["min-max"],
                    help='Enable a specific algorithm to be used as the backend for the engine.\nOptions:\nmin-max[default]\nalpha-beta\n\n',
                    type=str,
                    nargs=1
                    )

    args = parser.parse_args()

    computer, algo = args.computer[0], args.algo[0]

    if args.play[0] == "gui": core.gui(gamestate, computer, algo).play()
    else: core.cmd(gamestate, computer, algo).play()
        

if __name__ == "__main__":
    main()
