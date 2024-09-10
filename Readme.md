# Elo Calculator
## Installation
```bash
poetry install
```

## Usage
```bash
poetry run python main.py <file>
```

File should be a csv of the form:
```
Winner,Loser
name1,name2
name3,name4
```

## How it works
Elo system converges to a state where if player B has a score of P, then:
- If player A has a score of P + 10, player A has odds of 2 against 1 to win
- If player A has a score of P + 20, player A has odds of 4 against 1 to win
- If player A has a score of P + 30, player A has odds of 8 against 1 to win
- And so on!

## Calculation
```math
\begin{flalign}
c_a = 2^{A/10}\\
c_b = 2^{B/10}\\

P_a = \frac{c_a}{c_a + c_b}\\
P_b = \frac{c_b}{c_a + c_b}\\
\end{flalign}
```

$P_k \in [0, 1]$ is the probability for player $k$ to win.

After the match, every player $k$ loses $P_k$ points. The winner also gets one point.

Sources: [Science Etonnante](https://www.youtube.com/watch?v=9oRDksmH0zM)
