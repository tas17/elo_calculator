import pandas as pd
import typer


INITIAL_ELO = 100
DEFAULT_ELO = 10
QUOTE = 2
ROUNDING = 1
SEPARATOR = ","


ELOS = {}
def get_elo(name):
    if name not in ELOS:
        ELOS[name] = INITIAL_ELO
    return ELOS[name]

def set_elo(name, value):
    ELOS[name] = value


def main(infile: str, initializer_file: str | None = None):
    with open(infile) as f:
        lines = f.readlines()
    for line in lines[1:]:
        winner, looser = line.rstrip('\n').split(SEPARATOR)
        winner_elo = get_elo(winner)
        looser_elo = get_elo(looser)

        c_w = 2**(winner_elo)/DEFAULT_ELO
        c_l = 2**(looser_elo)/DEFAULT_ELO

        p_w = c_w / (c_w + c_l)
        p_l = c_l / (c_w + c_l)

        new_winner_elo = winner_elo + 1 - p_w
        new_looser_elo = looser_elo - p_l
        print(f"{winner} ({round(winner_elo, ROUNDING)}) wins against {looser} ({round(looser_elo, ROUNDING)}). New elos: {round(new_winner_elo, ROUNDING)} - {round(new_looser_elo, ROUNDING)}")

        set_elo(winner, new_winner_elo)
        set_elo(looser, new_looser_elo)

    print("\nRatings")
    for i, (name, elo) in enumerate(sorted(ELOS.items(), key=lambda x: -x[1])):
        print(f"- {i+1}) {name} ({round(elo, ROUNDING)})")


if __name__ == "__main__":
    typer.run(main)


