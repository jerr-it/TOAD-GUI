import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt

sns.set_theme(style="darkgrid")

df = pd.read_csv("../data/wfcmem.csv")
df["Peak"] = df["peak"]
df["Current"] = df["current"]

ax = sns.lineplot(data=df[["Peak", "Current"]].copy(), palette="Paired", linewidth=2.5)
ax.set_ylabel("Memory [B]")
ax.set_xlabel("Iteration []")

plt.show()