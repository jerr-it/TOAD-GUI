"""
Requires https://github.com/matthewjwoodruff/pareto.py
"""

import pareto
import pandas as pd

df: pd.DataFrame = pd.read_csv("../data/metrics.csv")

df["runtime_per_try"] = df["Runtime"] / df["Tries"]
df["tpkl_change"] = (df["TPKL Original-Fixed"] - df["TPKL Original-Generated"])
df["variation_change"] = (df["Pattern variation fixed"] - df["Pattern variation generated"])
df["difficulty_change"] = (df["Difficulty fixed"] - df["Difficulty generated"])

df2 = df[["patcher", "Runtime", "Peak memory", "Tries", "tpkl_change", "variation_change", "difficulty_change"]].copy()

goals = ["Runtime", "Peak memory", "Tries", "tpkl_change", "variation_change", "difficulty_change"]
goal_set = [i+1 for i in range(len(goals))]

df2: pd.DataFrame = df2.groupby("patcher").mean().reset_index()

df2["Runtime"] = df2["Runtime"].abs()
df2["Peak memory"] = df2["Peak memory"].abs()
df2["Tries"] = df2["Tries"].abs()
df2["tpkl_change"] = df2["tpkl_change"].abs()
df2["variation_change"] = df2["variation_change"].abs()
df2["difficulty_change"] = df2["difficulty_change"].abs()

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df2)

def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1, 1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]


for ps in sorted(powerset(goal_set), key=lambda x: len(x)):
    if len(ps) == 1:
        continue
    dfcopy = df2.copy()
    rank = 1
    goals_str = [goals[ps[i]-1] for i in range(len(ps))]
    print(f"\n\n-----Optimizing: {goals_str} ---------")
    while not dfcopy.empty:
        dist = pareto.eps_sort([list(dfcopy.itertuples(False))], ps)

        print(f"Rank {rank}")
        for elt in dist:
            # Remove the row from the df2 where the patcher is the same as the one in elt
            dfcopy = dfcopy[dfcopy["patcher"] != elt[0]]
            print(f"{elt[0]}, ", end="")

        print()
        rank += 1