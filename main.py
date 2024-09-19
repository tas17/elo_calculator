import pandas as pd
import typer
from datetime import date as date_calculator


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
        p1, p2, score, date, *rest = line.rstrip('\n').split(SEPARATOR)
        if score == "1-0":
            winner = p1
            looser = p2
        elif score == "0-1":
            winner = p2
            looser = p1
        elif score == "1-1":
            winner = None
            looser = None
        else:
            raise ValueError(f"Unexpcted value for {score=}")

        if winner:
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
        else:
            p1_elo = get_elo(p1)
            p2_elo = get_elo(p2)

            c_1 = 2**(p1_elo)/DEFAULT_ELO
            c_2 = 2**(p2_elo)/DEFAULT_ELO

            p_1 = c_1 / (c_1 + c_2)
            p_2 = c_2 / (c_1 + c_2)

            new_p1_elo = p1_elo + 0.5 - p_1
            new_p2_elo = p2_elo + 0.5 - p_2

            print(f"Draw between {p1} ({round(p1_elo, ROUNDING)}) and {p2} ({round(p2_elo, ROUNDING)}). New elos: {round(new_p1_elo, ROUNDING)} - {round(new_p2_elo, ROUNDING)}")

            set_elo(p1, new_p1_elo)
            set_elo(p2, new_p2_elo)

    print(f"\nRatings ({date_calculator.today()})")
    for i, (name, elo) in enumerate(sorted(ELOS.items(), key=lambda x: -x[1])):
        print(f"- {i+1}) {name} ({round(elo, ROUNDING)})")


if __name__ == "__main__":
    typer.run(main)


