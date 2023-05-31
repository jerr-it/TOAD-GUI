from matplotlib import pyplot as plt

from graphs import load_metrics_df
from graphs import PATCHER_NAMES

metrics_df = load_metrics_df()

for i, patcher in enumerate(PATCHER_NAMES):
    patcher_df = metrics_df[metrics_df["patcher"].str.contains(patcher)]
    patcher_df["Peak memory"] = patcher_df["Peak memory"] / 1000000
    patcher_df["Peak memory"].hist(bins=50, ax=plt.subplot(2, 5, i + 1))
    plt.xlabel("Peak memory (MB)")
    plt.ylabel("Frequency")
    plt.title(f"Peak memory ({patcher})")
    plt.tight_layout()
    plt.gcf().set_size_inches(10, 10)

for i, patcher in enumerate(PATCHER_NAMES):
    patcher_df = metrics_df[metrics_df["patcher"].str.contains(patcher)]
    patcher_df["Peak memory"] = patcher_df["Peak memory"] / 1000000

    mean = patcher_df["Peak memory"].mean()
    median = patcher_df["Peak memory"].median()

    plt.subplot(2, 5, i + 6)
    plt.bar(["Mean", "Median"], [mean, median])
    plt.annotate(f"{mean:.2f}", (0, mean), ha="center", va="bottom")
    plt.annotate(f"{median:.2f}", (1, median), ha="center", va="bottom")

    plt.ylabel("Peak memory (MB)")
    plt.title(f"Peak memory ({patcher})")

plt.subplots_adjust(hspace=0.5)
plt.subplots_adjust(top=0.9, bottom=0.1)
plt.gcf().set_size_inches(20, 10)
plt.suptitle("Peak memory (tracemalloc)", fontsize=16)

plt.savefig("../data/peak_memory.png")
plt.show()
