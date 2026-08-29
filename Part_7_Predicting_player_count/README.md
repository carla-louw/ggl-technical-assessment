# Part 7: Predicting Player Count

Run `predict_player_count.py`. I have no experience using MLflow, so results print to console and the trained model is pickled to `player_count_model.pkl` for Part 8 to reuse.

**Unit of observation:** one row per `(CASINOID, GAMEID)` pair - how many distinct players has this game attracted at this casino.

**Features:** the game's `THEME`/`MECHANICS`/`TYPE` content flags, its Part 3
similarity cluster, the casino's Part 4 cohort, and `DAYS_LIVE`.

**Split:** a plain random 80/20 split.

**Target transform:** `PLAYER_COUNT` is heavily skewed, so the model is trained on `log1p(PLAYER_COUNT)` and predictions are inverted with `expm1` before reporting, so a handful of huge pairs don't dominate the loss and results are still reported in plain "number of players" units.

## Avoiding leakage

`TOTALWAGER`, `TOTALSPINS`, `NETWIN`, `AVEWAGER_PER_SPIN`, `AVEPAYOUT_PER_SPIN` are deliberately excluded. They only exist because players already played this exact pair, so using them as features would be predicting the outcome from the outcome. Everything used is independent of this pair's own play history: static game content,
this pair's fixed go-live date, and each side's cluster/cohort label.

## Baseline and results

| | MAE (players) | R² |
|---|---|---|
| Baseline (predict the average) | 28.4 | -0.018 |
| Model (RandomForestRegressor) | 24.7 | 0.125 |

Guessing "the average" gets you within about 28 players on a typical pair and  explains none of the variance (R² = -0.018 -> just slightly worse than the mean). The model cuts the average error by about 12% and explains ~12.5% of the
variance - a real, if modest, improvement. 

This model is not nearly good enough to be useful. If I had more time I would go back to to the start and re-evaluate my choice in target variables and feature engineering as a simple model switch and retrain would not suffice in improving the results. 

## What drives the prediction

Grouped feature importance (`RandomForestRegressor.feature_importances_`):

| Group | Importance |
|---|---|
| DAYS_LIVE | 0.39 |
| MECH | 0.21 |
| COHORT | 0.20 |
| THEME | 0.16 |
| GAME_CLUSTER | 0.03 |
| TYPE | 0.02 |

**Note:** `DAYS_LIVE` having such high importance is partly a mechanical effect, not a better signal. `PLAYER_COUNT` is a *cumulative* count of distinct players since launch - a game that's simply been live longer has had more calendar time to accumulate new players, independent of whether it's actually a better fit for that casino.

