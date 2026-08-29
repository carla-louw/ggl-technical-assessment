# Part 5: Recommendation System

## Part 5.1: Recommend games per casino
Casinos in the same cohort (Part 4) tend to share preferences, so a game's performance among a casino's cohort peers is a reasonable proxy for how it would perform at that casino too. Score a game for a cohort as its total wagers and spins for casinos in that cohort (proxies for deposits and engagement). If a game has no history in the cohort yet, fall back to the average of its game cluster.

## Limitations

- Recommendations are cohort-level, not casino-level - two casinos in the same cohort get identical rankings. 
- The wagers and spins are combined via an unweighted average of independently min-max-scaled values. They are arbitrarily treated as equally important. 

## Part 5.2: Ranked output for a few example casinos

Three casinos from three different cohorts, to show recommendations
genuinely differ by casino profile. Direct cohort-score matches are rare
overall (see Limitations) - `CASINO_111` (Cohort 2) is one of the few
casinos where the direct scoring path shows up at all in the top 10.

`CASINO_111` (Cohort 2):
```
GAME_5461  0.571  Performs well with casinos in your cohort
GAME_5904  0.498  Performs well with casinos in your cohort
GAME_5586  0.423  Performs well with casinos in your cohort
GAME_4915  0.325  No cohort history yet, estimated from similar games
GAME_4913  0.325  No cohort history yet, estimated from similar games
```

`CASINO_103` (Cohort 0):
```
GAME_4835  0.771  No cohort history yet, estimated from similar games
GAME_4838  0.771  No cohort history yet, estimated from similar games
GAME_3750  0.771  No cohort history yet, estimated from similar games
GAME_3493  0.771  No cohort history yet, estimated from similar games
GAME_3496  0.771  No cohort history yet, estimated from similar games
```

`CASINO_15` (Cohort 1):
```
GAME_4644  0.479  Performs well with casinos in your cohort
GAME_2631  0.439  No cohort history yet, estimated from similar games
GAME_5454  0.439  No cohort history yet, estimated from similar games
GAME_4139  0.439  No cohort history yet, estimated from similar games
GAME_4024  0.439  No cohort history yet, estimated from similar games
```
