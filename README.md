# ggl-technical-assessment
Public repo for my GGL technical assessment: Casino Game Recommendation &amp; Predictive Modelling

## Clone & Data Setup

Clone the repo:

```bash
git clone https://github.com/carla-louw/ggl-technical-assessment.git
cd ggl-technical-assessment
```

`Data/` is excluded from version control (see `.gitignore`) since the raw files are large. Before running anything, create the following folders and place the three provided CSVs in `Data/Raw/`:

```
Data/Raw/dim_currency.csv
Data/Raw/dim_game.csv
Data/Raw/fact_activity.csv
Data/Formatted/    (empty - Part 1 writes here)
Data/Clean/        (empty - Part 2 writes here)
```

## Setup

```bash
python -m venv .venv
source .venv/Scripts/activate      # Windows Git Bash; use .venv/bin/activate on macOS/Linux
pip install -r requirements.txt
```

Run each part in order from the repo root - later parts depend on earlier parts' output files:

```bash
python Part_1_Data_modelling/model.py                          # Data/Raw -> Data/Formatted/player_activity_formatted.csv
python Part_2_EDA/eda.py                                       # Data/Formatted -> Data/Clean/player_activity_clean.csv
python Part_3_Game_similarity/game_similarity.py               # -> Part_3_Game_similarity/game_clusters.csv
python Part_4_Casino_cohorts/casinos.py                        # -> Part_4_Casino_cohorts/casino_clusters.csv
python Part_5_Recommendation_system/recommend_games.py
python Part_7_Causal_analysis/causal.py
python Part_7_Predicting_player_count/predict_player_count.py  # -> player_count_model.pkl
python Part_8_Scoring_scenario/score_new_game.py                # needs Part 7's pickled model
```
# Part 1 — Data Modelling

See README in work folder.

# Part 2 — Exploratory Data Analysis

See README in work folder.

# Part 3 — Game Similarity

See README in work folder.

# Part 4 — Casino Cohorts

See README in work folder.

# Part 5 — Recommendation System

See README in work folder.

# Part 6 — Evaluating the Recommendation System

## Evaluating during development:

Given the nature of the data a temporal holdout isn't possible as activity data only spans two days. I'd use the leave-one-out method: hide a game a casino already plays, add it back to the candidate pool, and check whether the recommender surfaces it again, benchmarked against a popularity baseline (randomness i.e. the average). 

## Evaluating during production:

I'd track adoption rate (% of recommended games a casino actually goes live with) and run an A/B test (recommended casinos vs a popularity-only control) and measuring post-launch wager/spins uplift. I'd also monitor ranking drift over time to decide on a retraining cadence.

## Risks:

- Popularity bias/feedback loops (recommending the same big games reinforces their lead)
- Sparse casino cohorts can produce noisy averages

# Part 7 — Causal Analysis

See README in work folder.

# Part 7 — Predicting Player Count

See README in work folder.

# Part 8 — Scoring Scenario

See README in work folder.

# Part 9 — Production & Operations

## 1. Deployment & Serving

The three models serve different purposes, so I'd deploy and serve them differently.

### Game Recommender and Player-Prediction Model

These models will be used by operators when reconfiguring existing casinos or configuring new casinos. It can be exposed to operators via the existing Player Account Management (PAM) backoffice system UI.

For the game recommender, pre-run model results, i.e. game predictions, can either be:

- Stored in the database (like Postgres) and queried via an API call when triggered by the operator, or
- Generated as a live prediction (also via API call) from a model deployed alongside the backoffice system.

The player-prediction model can only be called on via the latter.

In both cases the predicted result is returned to the operator via API call and displayed in the UI.

Since this isn't time-critical (it's a config decision, not a live intervention), batch is the natural default here. 

### Causal Model

This model needs to trigger automatically during a player's session. It can't sit inside the backoffice itself — the backoffice is built for admin/config workflows, not high-throughput low-latency inference on a live event stream. It needs to be deployed as its own real-time inference service, since the result has to trigger a cascade of events ending in an intervention during play (e.g. a free game award), and there's no room for delay.

Practically:

- The player buffer is streamed into the model in near real-time (e.g. via a message queue like Kafka), so features are always current.
- The model sits behind a low-latency synchronous API.
- A positive prediction triggers the intervention immediately.

Two things worth building in given the stakes:

- **Fallback behaviour**: if the service times out or is down, default to no intervention rather than blocking play, and log the failure for review.
- **Audit logging**: every prediction and resulting action gets logged, since these are live interventions during real-money play.

## 2. Monitoring & Retraining

### Game Recommender and Player-Prediction Model

- **Input/data monitoring**: feature drift (game catalog changes, new casinos, changing player demographics), and pipeline freshness — is the batch job actually completing on schedule.
- **Output monitoring**: distribution of recommendations (if it's suddenly recommending the same 3 games to everyone, that's a red flag), and operator acceptance/override rate as a proxy for usefulness.
- **Retraining trigger**: mostly time-based (monthly/quarterly), since this isn't safety-critical, plus ad hoc retraining when new games or casinos are added.

### Causal Model

- **Input/data monitoring**: player buffer feature drift, missing/late features, upstream pipeline health.
- **Output monitoring**: intervention trigger rate over time, prediction confidence distribution, latency/error rates on the live service.
- **Ground truth monitoring**: our actual goal here is player retention, so the real label comes after the fact.
  - Intervention followed by an extended session / player retained means the intervention was correct.
  - Intervention followed by player churn shortly after means the intervention was wrong or badly timed.
  - So the core ground-truth metric to track is post-intervention retention rate, not just trigger rate, since trigger rate on its own doesn't tell us if we intervened correctly.
- **Retraining trigger**: trigger-based rather than purely calendar-based — a sustained drop in post-intervention retention, or drift in input features, should kick off retraining.

## 3. Operational Risk

- **Model degradation/drift** — all three models can go stale as player behaviour or the game catalog shifts.
 *Mitigation*: the monitoring above, plus scheduled model reviews.

- **Pipeline/data failures** — missing or delayed features, especially the live player buffer feeding the causal model.
 *Mitigation*: upstream data validation and the fallback already mentioned — no intervention rather than acting on stale/incomplete data.

- **Latency/availability risk on the real-time service** — if the causal model service is slow or down, interventions don't fire in time.
 *Mitigation*: route through existing NOC incident monitoring, since NOC is already set up for uptime alerts.

- **Responsible gambling/regulatory risk** — this is the one I'd weigh most heavily given the domain. A missed or incorrect intervention isn't just a bad metric, it directly affects a player and sits inside our responsible-gambling obligations. Two failure directions matter:
  - **False negative** (should have intervened, didn't) can lead to risk of a harmful play pattern continuing unaddressed.
  - **False positive** (intervened unnecessarily) can lead to unnecessary cost (free game awarded), and overuse can undermine trust in the intervention system.
 *Mitigation*: audit logging of every prediction and action taken, human review for disputed/edge cases, and periodic compliance audits of intervention accuracy.

# Part 10: Business Judgement & Data

## 1. Emerging Casinos

The signal for emerging casinos is higher traffic than other casinos of a similar nature. There are actually two signals here: number of players, and number of spins.

The pitfall is that these signals, this early in a casino's life, aren't an indication of player retention or true player value, which is the ultimate goal. High traffic early on can look like promise but tell us nothing about whether those players stick around or become valuable long-term — so on their own, these signals are more noise than signal for what actually matters.

## 2. Increasing Reach

Growth in a casino translates to three things: increased registration numbers, increased deposits, and player retention — players coming back for a second, third, fourth session instead of dropping off after the first, which is what we often see.

The game recommender and player-prediction models can indicate to a casino if there are gaps in the variety they offer players, compared to other similar casinos. The causal model can indicate the underlying causes affecting spins and wagering, which is a proxy for deposits.

An increase in any of the three signals above (registrations, deposits, retention) can be taken as an indication of success.

## 3. Additional Data

Ideally, we'd model the player journey — both within sessions of play and across sessions.

Within-session, this includes all wagering and payout information across time i.e the full player buffer.

Across sessions, this includes depositing behaviour, withdrawal behaviour, churn, and session length, to name a few.

These features are all much better indicators of player value than what we currently have.
