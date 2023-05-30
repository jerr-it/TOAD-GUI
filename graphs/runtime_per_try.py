from matplotlib import pyplot as plt

from graphs import load_metrics_df
from graphs import PATCHER_NAMES

metrics_df = load_metrics_df()

for i, patcher in enumerate(PATCHER_NAMES):
    patcher_df = metrics_df[metrics_df["patcher"].str.contains(patcher)]
    patcher_df["Runtime"] = patcher_df["Runtime"] / patcher_df["Tries"]
    patcher_df["Runtime"].hist(bins=50, ax=plt.subplot(2, 4, i + 1), range=(0, 50))
    plt.xlabel("Runtime (s)")
    plt.ylabel("Frequency")
    plt.title(f"Runtime per try ({patcher})")
    plt.tight_layout()
    plt.gcf().set_size_inches(10, 10)

for i, patcher in enumerate(PATCHER_NAMES):
    patcher_df = metrics_df[metrics_df["patcher"].str.contains(patcher)]

    patcher_df["Runtime"] = patcher_df["Runtime"] / patcher_df["Tries"]

    mean = patcher_df["Runtime"].mean()
    median = patcher_df["Runtime"].median()

    plt.subplot(2, 4, i + 5)
    plt.bar(["Mean", "Median"], [mean, median])
    plt.annotate(f"{mean:.2f}", (0, mean), ha="center", va="bottom")
    plt.annotate(f"{median:.2f}", (1, median), ha="center", va="bottom")

    plt.ylabel("Runtime (s)")
    plt.title(f"Runtime per try ({patcher})")

plt.subplots_adjust(hspace=0.5)
plt.subplots_adjust(top=0.95, bottom=0.1)
plt.gcf().set_size_inches(20, 10)

plt.savefig("../data/runtime_per_try.png")
plt.show()
