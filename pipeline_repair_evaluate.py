import concurrent.futures
import os
import time
import tracemalloc

from patching import patchers
from patching.metrics import metrics

THREADS = 4


def list_generators() -> list[str]:
    """
    List all generators for which there are levels generated by the previous pipeline stage.
    :return: List of paths to all generators
    """
    base_path: str = os.path.join(os.path.curdir, "data")
    return os.listdir(base_path)


def benchmark(fn: callable):
    """
    Decorator to measure the runtime of a function.
    :param fn: Function to measure
    :return: Function result and runtime
    """
    def wrapper(*args, **kwargs):
        tracemalloc.start()

        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()

        _, peak = tracemalloc.get_traced_memory()

        tracemalloc.stop()

        return result, end - start, peak
    return wrapper


def save_metrics_to_file(generator_dir: str, data: dict):
    """
    Save a metrics as a csv file
    :param generator_dir: Path to the generator directory
    :param data: Metric data
    :param name: Name of the metric
    :return: None
    """
    with open(os.path.join(os.path.curdir, "data", generator_dir, "metrics.csv"), "w") as f:
        # Write header
        f.write("level,patcher,")

        for i in range(len(metrics)):
            f.write(f"{metrics[i]['name']}")

            if i < len(metrics) - 1:
                f.write(",")

        f.write("\n")

        # Write data
        for level_name, patcher_data in data.items():
            for patcher_name, metric_data in patcher_data.items():
                f.write(f"{level_name},{patcher_name},")

                for i in range(len(metrics)):
                    f.write(f"{metric_data[metrics[i]['name']]}")
                    if i < len(metrics) - 1:
                        f.write(",")

                f.write("\n")


def test_levels(generator_dir: str):
    """
    Test all levels generated by the previous pipeline stage.
    :param generator_dir: Path to the generator directory
    :return: None
    """
    level_files: list[str] = os.listdir(os.path.join(os.path.curdir, "data", generator_dir))

    # level_name -> (patcher_name -> (metric_name -> metric_value))
    metric_results = {}

    for level_file in level_files:
        # Ignore non-level files
        if not level_file.endswith(".txt"):
            continue

        level_path: str = os.path.join(os.path.curdir, "data", generator_dir, level_file)

        # Read level line by line
        level: list[str] = []
        with open(level_path, "r") as f:
            for line in f:
                level.append(line.rstrip())

        # First line is the progress the agent made, read and remove it
        progress: str = level[0]
        level = level[1:]

        # Level height is the number of lines in the level
        level_height: int = len(level)
        # Level width is the length of the first line
        level_width: int = len(level[0])

        progress_blocks: int = int(float(level_width) * float(progress))

        broken_range = (
            (max(progress_blocks - 5, 0), min(progress_blocks + 5, level_width)),
            (0, level_height)
        )

        if level_file not in metric_results:
            metric_results[level_file] = {}

        # Iterate available patchers
        for patcher_name, patcher in patchers.items():
            print(f"Repairing {level_file} with {patcher_name}...")

            if patcher_name not in metric_results[level_file]:
                metric_results[level_file][patcher_name] = {}

            for metric in metrics:
                metric["object"].pre_hook()

            patched_section = patcher.patch(level, broken_range)

            for metric in reversed(metrics):
                result = metric["object"].post_hook(patched_section)

                metric_results[level_file][patcher_name][metric["name"]] = result

    save_metrics_to_file(generator_dir, metric_results)


def pipeline_repair_evaluate():
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = [
            executor.submit(
                test_levels,
                generator_path
            )
            for generator_path in list_generators()
        ]

        for future in concurrent.futures.as_completed(futures):
            pass


pipeline_repair_evaluate()
