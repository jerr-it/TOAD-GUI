from patching.metrics.coins import Coins
from patching.metrics.collected_mushrooms import CollectedMushrooms
from patching.metrics.difficulty import Difficulty, RollingDifficulty
from patching.metrics.hits import Hits
from patching.metrics.jump_air_time import JumpAirTime
from patching.metrics.jump_length import JumpLength
from patching.metrics.jumps import Jumps
from patching.metrics.lives import Lives
from patching.metrics.memory import Memory
from patching.metrics.metric import Metric
from patching.metrics.pattern_variation import PatternVariation
from patching.metrics.remaining_time import RemainingTime
from patching.metrics.runtime import Runtime
from patching.metrics.total_kills import TotalKills
from patching.metrics.tpkl import TPKL
from patching.metrics.tries import Tries

metrics: list[Metric] = [
    RollingDifficulty(),
    # CollectedMushrooms(),
    # Coins(),
    # TotalKills(),
    # Jumps(),
    # Lives(),
    # JumpAirTime(),
    # JumpLength(),
    # Hits(),
    # RemainingTime(),
    PatternVariation(),
    Tries(),
    Difficulty(),
    TPKL(),
    Memory(),
    Runtime(),
]
