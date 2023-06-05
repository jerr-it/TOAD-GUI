import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from graphs import load_metrics_df, add_generator_column, add_cumul_difficulty_column

sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
metrics_df: pd.DataFrame = load_metrics_df()

metrics_df = add_generator_column(metrics_df)
metrics_df = add_cumul_difficulty_column(metrics_df)
metrics_df = metrics_df.sort_values(by="generator")
df = metrics_df[["generator", "Difficulty generated"]].copy()

pal = sns.cubehelix_palette(15, rot=-.25, light=.7)
g = sns.FacetGrid(df, row="generator", hue="generator", aspect=15, height=.5, palette=pal)

g.map(sns.kdeplot, "Difficulty generated",
      bw_adjust=.5, clip_on=False,
      fill=True, alpha=1, linewidth=1.5)
g.map(sns.kdeplot, "Difficulty generated", clip_on=False, color="w", lw=2, bw_adjust=.5)

g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)


def label(x, color, label):
    ax = plt.gca()
    ax.text(0, .2, label, fontweight="bold", color=color,
            ha="left", va="center", transform=ax.transAxes)


g.map(label, "Difficulty generated")

# Set the subplots to overlap
g.figure.subplots_adjust(hspace=-.25)

# Remove axes details that don't play well with overlap
g.set_titles("")
g.set(yticks=[], ylabel="")
g.despine(bottom=True, left=True)

plt.show()