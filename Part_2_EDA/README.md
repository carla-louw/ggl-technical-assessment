# Part 2: Exploratory Data Analysis

**Disclaimer:** Very limited EDA was done due to time constraint.

## Part 2.1: Check for missing values
**Purpose:** Check for any missing values in the dataset. Missing values need to be addressed before a machine learning project can proceed.

**Outcome:** There are no missing values in the dataset, so no mitigating steps need to be taken.

## Part 2.2: Check for duplicated values
**Purpose:** Check for any duplicated entries in the dataset. Duplicated entries can skew the training of a machine learning model and need to be dropped from the dataset prior to model training.

**Outcome:** There are no duplicated entries in the dataset.

## Part 2.3: Check for columns with no variance
**Purpose:** Data fields that contain entries of only one value will not be translated to a meaningful feature upon model training and can be dropped from the dataset.

**Outcome:** 129 columns were dropped from the dataset, all of the groups: GAMETYPE, MECHANICS, and THEME.

## Part 2.4: Add average wager and average payout
**Method:** Calculate proxy features for player value (AVEWAGER_PER_SPIN and AVEPAYOUT_PER_SPIN) by dividing TOTALWAGER and TOTALPAYOUT by TOTALSPINS.

**Purpose:** Player behaviour during a playing session differs based on player type. One key distinction between player types is player value. The behaviour of low value players (like the classic $1 players) differ greatly from high value players (whales). The existing monetary data fields (TOTALWAGER and TOTALPAYOUT) alone make it difficult to infer player value.

## Part 2.5: Statistical summary
**Purpose:** Firstly check for the general spread of the data, do we have any outliers or skewed data. These phenomona can affect the performance and accuracy of ML models. Secondly check for any anomalies in the data, for example like negative entries when all entries should be non-negative.

**Outcome:** The spread of the data is as is expected for casino data: all of the monetary values are right-skewed. The only apotential anomaly is the presence of TOTALWAGER entries with a value of zero. However, this can also be free game offers that the player received. 

## Part 2.6: Total Wager and Total Payout vs Total Spins
**Purpose:** Check whether spin volume alone explains how much is wagered/paid out, or whether wager and payout are driven by more than just how many spins a row represents.

**Outcome:** Most rows sit near the origin (low spins, low amount), consistent with the right-skew already noted in Part 2.5. Wager and Payout closely overlap at almost every spin count across the whole chart, not just on average - they track each other very tightly (see Part 7's causal analysis). 

## Known limitation: this skew is structural, not noise

Every distribution examined here - individual wagers, casino totals, and (by strong implication) player value - is heavily right-skewed in the same way. This is a known, expected property of gambling data: a small number of high-value players/casinos genuinely account for a disproportionate share of activity. **These are not outliers to be dropped** - they are a real, distinct population (whales), and removing them would throw away the signal that matters most commercially, not noise.

For time reasons, this submission does not split or otherwise treat that skew in the data - wager/spins are scaled where needed (Parts 3-5), but high-value and low-value players/casinos are still pooled into the same distributions, cohorts, and models throughout. With more time, the right fix is an explicit segmentation, e.g. splitting high-value from low-value player/casino data and modelling each population separately, since a single pooled average or model is liable to either be dominated by the tail or fail to represent it well, depending on the method.
