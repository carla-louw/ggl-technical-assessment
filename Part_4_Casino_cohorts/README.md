# Part 4: Casino Cohorts

## Part 4.1: Prepare casino-level features

I characterised each casino by:
- Which game clusters (from Part 3) it has exposure to.
- Which currencies it transacts in.

**Rationale:** a casino's *preferences* are best captured by the variety of game types and currencies it offers to players.

## Part 4.2: Fit KMeans clustering

Use an elbow plot to determine the optimal number of clusters (in this case 8). Fit KMeans clustering and export results as a csv.

## Part 4.3: Cohort profiles

| Cohort | Casinos | Avg wager | Avg net win | Currencies used | Game clusters played |
|---|---|---|---|---|---|
| 0 | 15 | 277,092 | 12,203 | 3.8 | 11.0 |
| 1 | 24 | 318,764 | 11,164 | 4.9 | 17.7 |
| 2 | 22 | 215,798 | -17,292 | 1.2 | 7.4 |
| 3 | 16 | 64,174 | -7,175 | 1.3 | 1.8 |
| 4 | 12 | 183,730 | 10,076 | 4.2 | 16.3 |
| 5 | 12 | 155,989 | 12,543 | 1.1 | 15.0 |
| 6 | 20 | 279,627 | 16,993 | 1.2 | 15.9 |
| 7 | 8 | 181,614 | 10,800 | 5.9 | 23.6 |

- **Cohort 0 - Moderate multi-currency casinos (15).** Decent currency
  spread (3.8) and catalogue breadth (11.0), solid wager and net win.
- **Cohort 1 - Broad, high-value casinos (24, the largest group).** Highest
  currency support (4.9, second only to Cohort 7) and wide catalogue (17.7),
  with the second-highest wager of any cohort.
- **Cohort 2 - Single-currency casinos running at a loss (22).** Narrow
  currency (1.2) and catalogue (7.4), and the worst net win of any cohort
  (-17,292). Worth investigating directly - broad-based issue or a few large
  payout events.
- **Cohort 3 - Small, single-game-focused, net-loss casinos (16).** By far
  the narrowest catalogue of any cohort (1.8 game clusters - essentially
  single-game shops), lowest wager volume, and also running at a net loss
  (-7,175).
- **Cohort 4 - Moderate-to-broad multi-currency casinos (12).** Similar
  shape to Cohort 1 (multi-currency, broad catalogue) but smaller scale.
- **Cohort 5 - Single-currency casinos with wide catalogues (12).** Narrowest
  currency support of any cohort (1.1) but broad game variety (15.0), with a
  solid net win (12,543) - focused on one payment method, not on games.
- **Cohort 6 - Single-currency, high-value, best-margin casinos (20).** High
  wager (279,627) and the best net win of any cohort (16,993), despite
  single-currency focus (1.2).
- **Cohort 7 - Broadest, most diversified casinos (8, the smallest group).**
  Widest currency support (5.9) and widest game variety (23.6) of any
  cohort, by a clear margin.

**Note:** There are many valid ways to define cohorts. These results are passable as a first attempt, and the resulting cohorts do make sense, but with more time I'd put more thought into how the cohorts are actually built. What the "right" definition even is depends a lot on what the cohorts are for. I built features from currency and game-cluster exposure, then interpreted the resulting clusters using monetary values. It could just as easily be flipped - cluster directly on the monetary/performance metrics, then interpret those clusters by their currency/game preferences instead. 