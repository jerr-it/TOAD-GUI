import concurrent.futures
import os

import pandas as pd

from patching import patchers
from patching.metrics import metrics
from utils.mario_ai import MarioAI

REPAIR_STAGE_THREADS = 8


def list_generators() -> list[str]:
    """
    List all generators for which there are levels generated by the previous pipeline stage.
    :return: List of paths to all generators
    """
    files: list[str] = []
    basepath: str = os.path.join(os.path.curdir, "data")

    with os.scandir(basepath) as it:
        for entry in it:
            if entry.is_dir():
                files.append(str(entry.name))

    return files


def list_levels(generator_path: str) -> list[str]:
    """
    Lists all levels inside the given generators data directory
    :param generator_path: path to level files for a given generator
    :return: list of levels to be tested inside that directory (path
    """
    level_files: list[str] = []

    with os.scandir(generator_path) as it:
        for entry in it:
            if entry.name.startswith("level"):
                path = os.path.join(generator_path, str(entry.name))
                level_files.append(path)

    return level_files


def parse_broken_level(level_path: str) -> (list[str], float):
    """
    Parses a file containing a broken level
    Always contains the mario agents progress in the first line.
    All other following lines are rows of the level
    :param level_path:
    :return:
    """
    level: list[str]
    progress: float

    with open(level_path, "r") as f:
        lines = f.readlines()
        progress = float(lines.pop(0))
        level = [line.rstrip() for line in lines]

    return level, progress


def already_done(level_path: str, patcher: str, metrics_df: pd.DataFrame) -> bool:
    """
    Returns true if we already ran the given patcher on the given level
    :param level_path: path to the level
    :param patcher: patcher to apply
    :param metrics_df: df containing already completed runs
    :return: True if the patcher was already run on that level
    """
    return ((metrics_df["level"] == level_path) & (metrics_df["patcher"] == patcher)).any()


def load_original_level(generator_path: str) -> list[str]:
    """
    Loads the original level the given generator was trained on
    :param generator_path: Path to the generator
    :return: Original level the generator was trained on
    """
    level_id: str = generator_path.split("_")[2]
    level_path: str = os.path.join(os.path.curdir, "levels", "originals", f"lvl_{level_id}.txt")

    level: list[str]
    with open(level_path, "r") as f:
        level = [line.rstrip() for line in f.readlines()]

    return level


def calculate_broken_range(
        progress: float,
        level_width: int,
        level_height: int,
        range_width: int = 5
) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Calculates a range thats to be replaced by the patcher
    :param progress: Progress the mario agent made in %
    :param level_width: Total width of the level (blocks)
    :param level_height: Total height of the level (blocks)
    :param range_width: How wide the range is supposed to be in each direction
    :return: Range
    """
    block_progress = int(float(level_width) * progress)

    return (
        (max(block_progress - range_width, 0), min(block_progress + range_width, level_width - 2)),
        (0, level_height)
    )


def repair_level(
        level_path: str,
        generator_path: str,
        metrics_df: pd.DataFrame
) -> (str, pd.DataFrame, dict[str, list[str]]):
    """
    Repairs a given broken level using all available repair mechanisms and
    evaluates their performance with the given metrics
    :param level_path: Path to the level thats to be repaired
    :param generator_path: Path to the generator the level was created from
    :param metrics_df: Existing metrics data, to avoid repairing a level twice
    :return: (
        Dataframe containing metrics evaluated on the different patchers,
        dict of levels fixed (one per patcher)
    )
    """
    level, progress = parse_broken_level(level_path)
    level_width: int = len(level[0])
    level_height: int = len(level)

    original_level = load_original_level(generator_path)

    broken_range = calculate_broken_range(progress, level_width, level_height)

    with MarioAI() as mario:
        metrics_data = []
        level_dict = {}

        for patcher_name, patcher in patchers.items():
            if already_done(level_path, patcher_name, metrics_df):
                print(f"Skipping {patcher_name} for {level_path}")
                continue

            print(f"Applying patcher {patcher_name} to {level_path}")
            metrics_data.insert(0, {"level": level_path, "patcher": patcher_name})

            for metric in metrics:
                metric["object"].pre_hook()

            # TODO loop until playable
            fixed_level: list[str] = patcher.patch(original_level, level, broken_range)
            progress = mario.evaluate_level(fixed_level)

            level_dict[patcher_name] = fixed_level
            for metric in reversed(metrics):
                result = metric["object"].post_hook(original_level, level, fixed_level)
                metrics_data[0][metric["name"]] = result

    return level_path, pd.DataFrame(metrics_data), level_dict


def read_or_create_metrics_csv() -> pd.DataFrame:
    metrics_path: str = os.path.join(os.path.curdir, "data", "metrics.csv")
    metrics_df: pd.DataFrame()

    if os.path.exists(metrics_path):
        metrics_df = pd.read_csv(metrics_path)
    else:
        headers = ["level", "patcher"]
        for metric in metrics:
            headers.append(metric["name"])
        metrics_df = pd.DataFrame(columns=headers)

    return metrics_df


def save_patched_level(level_path: str, patcher_name: str, level: list[str]):
    tag = patcher_name.replace(" ", "_").lower()
    patched_path = level_path.replace("level", f"patched_{tag}")
    with open(patched_path, "w") as f:
        for row in level:
            f.write(row + "\n")


def pipeline_repair_evaluate():
    metrics_df = read_or_create_metrics_csv()

    generators = list_generators()
    generator_count = len(generators)

    for idx, generator_name in enumerate(generators):
        print(f"Fixing levels in {generator_name} ({idx+1}/{generator_count})")

        generator_path: str = os.path.join(os.path.curdir, "data", generator_name)

        level_files: list[str] = list_levels(generator_path)
        level_file_count: int = len(level_files)

        level_idx = 1
        with concurrent.futures.ThreadPoolExecutor(max_workers=REPAIR_STAGE_THREADS) as executor:
            futures = [
                executor.submit(repair_level, level_path, generator_path, metrics_df)
                for level_path in level_files
            ]

            for future in concurrent.futures.as_completed(futures):
                level_path, new_df, level_dict = future.result()
                metrics_df = pd.concat([metrics_df, new_df], ignore_index=True)

                for patcher_name, level in level_dict.items():
                    save_patched_level(level_path, patcher_name, level)

                metrics_df.to_csv(os.path.join(os.path.curdir, "data", "metrics.csv"), index=False)
                print(f"Completed level ({level_idx}/{level_file_count}) for {generator_name}")
                level_idx += 1


pipeline_repair_evaluate()
