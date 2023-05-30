from enum import Enum

import numpy as np
import py4j.java_gateway

from patching.patcher import Patcher


class GameStatus(Enum):
    RUNNING = 0,
    WIN = 1,
    LOSE = 2,
    TIME_OUT = 3


class Online(Patcher):
    """
    Not really 'online' patcher
    Tries to apply minimal changes to the level to make mario pass
    Places an X token to prevent a deadly jump
    Creates tunnels through obstacles too tall to jump over
    """
    def patch(
            self,
            original_level: list[str],
            level: list[str],
            broken_range: tuple[tuple[int, int], tuple[int, int]],
            generator_path: str = "",
            mario_result: py4j.java_gateway.JavaObject = None,
    ) -> list[str]:
        level = np.array([list(row) for row in level])

        mario_status = mario_result.getMarioStatus()
        status = mario_status.getStatus()
        if status == GameStatus.LOSE.value:
            # place an X token where mario died
            x = min(mario_status.getX(), len(level[0]))
            y = min(mario_status.getY(), len(level))
            level[y][x] = "X"

        elif status == GameStatus.TIME_OUT.value:
            # Remove the section ahead of mario with something guaranteed to be passable
            # Example:
            # --XXX      --XXX
            # --XXX  ->  -----
            # XX--X      XXXXX
            x = mario_status.getX()
            y = mario_status.getY()
            for xp in range(x+1, x+6):
                level[y][xp] = "-"
                level[y+1][xp] = "X"

        return ["".join(row) for row in level]
