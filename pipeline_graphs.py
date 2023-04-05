import os
import pandas as pd
import matplotlib.pyplot as plt

metrics = [
    {"name": "Runtime", "unit": "s"},
    {"name": "Memory", "unit": "MiB"}
]


def list_metric_files(metric: str) -> list[str]:
    """
    List all files for a given metric. Every metric has its own file.
    :param metric: Name of the metric
    :return: Paths to all files for the given metric
    """
    base_path: str = os.path.join(os.path.curdir, "data")
    file_names: list[str] = []

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file == metric + ".csv":
                file_names.append(os.path.join(root, file))

    return file_names


def aggregate_dataframes(file_names: list[str]) -> pd.DataFrame:
    """
    Aggregate all dataframes from the given files into one dataframe.
    CSV files are split, there is one per generator.
    :param file_names: File names to the CSV files
    :return: Aggregated dataframe
    """
    dataframes = []

    for file_name in file_names:
        dataframes.append(pd.read_csv(file_name))

    return pd.concat(dataframes)


for metric in metrics:
    file_names: list[str] = list_metric_files(metric["name"])
    data: pd.DataFrame = aggregate_dataframes(file_names)

    grouped = data.groupby("patcher")[["value"]].agg(["mean", "var"])

    # Plot the data
    ax = grouped.plot.bar(yerr=grouped["value"]["var"], capsize=4)
    ax.set_ylabel(metric["name"] + " (" + metric["unit"] + ")")
    ax.set_xlabel("Patcher")
    ax.set_title("Mean and variance of " + metric["name"] + " per patcher")

    plt.show()
