"""
Generates unplayable levels for all generators.
"""

import concurrent.futures
import os
import pandas as pd

from datetime import datetime

from utils.mario_ai import MarioAI
from utils.toad_gan_utils import load_trained_pyramid, generate_sample, TOADGAN_obj
from utils.level_utils import one_hot_to_ascii_level, place_a_mario_token

LEVEL_WIDTH = 202
LEVEL_HEIGHT = 16
LEVELS_PER_GENERATOR = 8
GENERATE_STAGE_THREADS = 8


def list_generators() -> list[str]:
    """
    Lists all generators.
    :return: List of generator names.
    """
    base_path: str = os.path.join(os.path.curdir, "generators", "v2")
    sub_folders: list[str] = os.listdir(base_path)

    directories = []
    for sub_folder in sub_folders:
        directories.append(os.path.join(base_path, sub_folder))

    return directories


def load_generator(path: str) -> TOADGAN_obj:
    """
    Loads the generator from the given path.
    :param path: Path to the generator.
    :return: Generator object.
    """
    return load_trained_pyramid(path)[0]


def generate_unplayable_level(generator: TOADGAN_obj) -> (list[str], float, int):
    """
    Generates an unplayable level.
    :param generator: Generator to use.
    :return: (level, progress, number of tries)
    """
    with MarioAI() as mario:
        scl_h = LEVEL_HEIGHT / generator.reals[-1].shape[-2]
        scl_w = LEVEL_WIDTH / generator.reals[-1].shape[-1]

        attempts = 0

        ascii_level: list[str] = []
        progress: float = 1.0

        while 1.0 - progress < 0.01:
            level, scales, noises = generate_sample(
                generator.Gs, generator.Zs, generator.reals,
                generator.NoiseAmp, generator.num_layers, generator.token_list,
                scale_h=scl_w, scale_v=scl_h
            )
            attempts += 1

            ascii_level = one_hot_to_ascii_level(level, generator.token_list)
            ascii_level = place_a_mario_token(ascii_level)
            ascii_level = remove_newlines(ascii_level)

            result = mario.evaluate_level(ascii_level)
            progress = result.getCompletionPercentage()

    return ascii_level, progress, attempts


def remove_newlines(level: list[str]) -> list[str]:
    lvl = []

    for line in level:
        lvl.append(line.rstrip())

    return lvl


def save_generated_level(level: list[str], progress: float, generator_path: str):
    """
    Saves the generated level to a file.
    :param level: Generated level.
    :param progress: Progress of the level. Saves time later on.
    :param generator_path: Path to the generator.
    :param number: Number of the level.
    :return: None
    """
    generator_name = os.path.basename(generator_path)

    level_path = os.path.join(os.path.curdir, "data", generator_name)
    os.makedirs(level_path, exist_ok=True)

    # Create time stamp as year_month_day_hour_minute_second_millisecond
    time_stamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")

    level_name = f"level_{generator_name}_{time_stamp}.txt"
    level_path = os.path.join(level_path, level_name)

    with open(level_path, "w") as f:
        f.write(f"{progress}\n")
        for row in level:
            f.write(row + "\n")


def pipeline_generate():
    generator_attempts = {}
    for generator_path in list_generators():
        total_attempts = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=GENERATE_STAGE_THREADS) as executor:
            futures = [
                executor.submit(
                    generate_unplayable_level,
                    load_generator(generator_path),
                )
                for _ in range(LEVELS_PER_GENERATOR)
            ]

            idx = 0
            for future in concurrent.futures.as_completed(futures):
                level, progress, attempts = future.result()

                save_generated_level(level, progress, generator_path)
                print(f"Saved level {idx} for {generator_path} with {attempts} attempts.")

                total_attempts += attempts
                idx += 1

        generator_attempts[generator_path] = total_attempts

    # Load attempts from data/attempts.csv or create a new one
    attempts_path = os.path.join(os.path.curdir, "data", "attempts.csv")
    if os.path.exists(attempts_path):
        attempts_df = pd.read_csv(attempts_path)
    else:
        attempts_df = pd.DataFrame(columns=["generator", "unplayable", "attempts", "share"])

    # Update generator entries with new attempts, unplayable level count and share
    for generator_path, total_attempts in generator_attempts.items():
        # Get the row from the csv file or create a new one
        if generator_path not in attempts_df["generator"].values:
            attempts_df.loc[len(attempts_df)] = {
                "generator": generator_path,
                "unplayable": 0,
                "attempts": 0,
                "share": 0.0
            }

        row = attempts_df.loc[attempts_df["generator"] == generator_path]

        # Update attempts, unplayable and share
        attempts_df.loc[attempts_df["generator"] == generator_path, "unplayable"] = row["unplayable"] + LEVELS_PER_GENERATOR
        attempts_df.loc[attempts_df["generator"] == generator_path, "attempts"] = row["attempts"] + total_attempts

        row = attempts_df.loc[attempts_df["generator"] == generator_path]

        attempts_df.loc[attempts_df["generator"] == generator_path, "share"] = row["unplayable"] / row["attempts"]

    # Sort rows by share descending
    attempts_df = attempts_df.sort_values(by=["share"], ascending=False)

    # Save attempts in data/attempts.csv
    attempts_df.to_csv(os.path.join(os.path.curdir, "data", "attempts.csv"), index=False)


pipeline_generate()
