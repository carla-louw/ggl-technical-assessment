# Part 3: Game Similarity

## Part 3.1: Build one feature row per game
For each game, build a feature vector from its THEME/MECHANICS/TYPE flags, scale with StandardScaler, then use NearestNeighbors to find the closest games by distance. Given a game, this returns a ranked list of its most similar games directly.

**Trade-off:** this only measures content similarity (what the game *is*), not behavioural similarity (how players actually respond to it). Two games could look similar on paper but perform completely differently. Didn't have time to blend in a behavioural signal (e.g. do the same players/casinos play both games), which would be the natural next step.

## Part 3.2: Examples & sanity check

For each worked example, the script checks how many THEME/MECH/TYPE flags the top match actually shares with the query game. All three top matches in the output share almost all (or all) of their attributes with the query game.

## Part 3.3: KMeans clustering 

I initially used KMeans clustering for this section and the cluster outputs were subsequently used in Parts 4 and 5. I later reworked this section to use NearestNeighbors, as Part 3.2 currently stands. I however did not have time to rework Part 3.3's clustering to be inferred from the NearestNeighbors output. Hence this section shows an older version of my code which is used for further analyses. 

An elbow plot was used to find the optimal number of clusters and the results are exported to a csv file.
