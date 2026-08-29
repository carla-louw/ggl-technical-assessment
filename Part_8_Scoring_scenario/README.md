# Part 8: Scoring Scenario

Run `score_new_game.py` - loads the model trained in Part 7
(`player_count_model.pkl`) and scores one cold-start pair.

## Worked example

**Game:** `GAME_4599`.
**Casino:** `CASINO_19` - does not currently offer this game.
**Question:** if launched at `CASINO_19`, how many distinct players would
`GAME_4599` likely attract?

**Result:** ~24.3 predicted distinct players on day one.

## Assumption and confidence

**Assumption:** `DAYS_LIVE` is set to `0` because this pair has never gone live - there's no real launch date to compute an age from. 

**Confidence: low-to-moderate.** R² = 0.125 on held-out pairs from Part 7. We also noted in Part 7 that `DAYS_LIVE` is the strongest signal for predicted number of players. Given that I set it to `0` the model could underestimate the target.
