import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

sns.set_theme()
df: pd.DataFrame = pd.read_csv("../data/attempts.csv")

df = df[["generator", "agent", "share"]].copy()

df = df.pivot(index="agent", columns="generator", values="share")

df = df.sort_values(df.first_valid_index(), axis=1)

row_averages = df.mean(axis=1)
col_averages = df.mean(axis=0)

vmin = df.values.min()
vmax = df.values.max()

fig, axs = plt.subplots(2, 2, figsize=(10, 8), gridspec_kw={'width_ratios': [1, 0.2], 'height_ratios': [1, 0.2]})

sns.heatmap(df, annot=True, cbar=False, ax=axs[0, 0], vmin=vmin, vmax=vmax)
axs[0, 0].set_title('Tries (mean)')

sns.heatmap(row_averages.to_frame(), annot=True, cbar=True, ax=axs[0, 1], vmin=vmin, vmax=vmax)
axs[0, 1].set_title('Row Averages')
axs[0, 1].set_ylabel("")

sns.heatmap(col_averages.to_frame().T, annot=True, cbar=False, ax=axs[1, 0], vmin=vmin, vmax=vmax)
axs[1, 0].set_title('')
axs[1, 0].set_xlabel("Column Averages")

axs[1, 0].set_xticks([])
axs[1, 0].set_yticks([])
axs[0, 1].set_xticks([])
axs[0, 1].set_yticks([])
axs[1, 1].set_xticks([])
axs[1, 1].set_yticks([])

plt.tight_layout()

plt.show()