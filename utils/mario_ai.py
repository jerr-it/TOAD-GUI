import os

import py4j.java_gateway
from py4j.java_gateway import JavaGateway

# old: MARIO_AI_PATH = os.path.abspath(os.path.join(os.path.curdir, "Mario-AI-Framework/mario-1.0-SNAPSHOT.jar"))
MARIO_AI_PATH = os.path.abspath(os.path.join(os.path.curdir, "Mario-AI-Framework/mario_ai_revisited.jar"))


class MarioAI:
    """
    Wraps using Py4j and the Mario AI Framework to be used with "with"
    """
    def __init__(self):
        self.gateway: JavaGateway

    def __enter__(self):
        self.gateway = JavaGateway.launch_gateway(
            classpath=MARIO_AI_PATH,
            die_on_exit=True,
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.gateway.java_process.kill()
        self.gateway.shutdown()

    def evaluate_level(self, level: list[str]) -> py4j.java_gateway.JavaObject:
        game = self.gateway.jvm.mff.agents.common.AgentMarioGame()
        agent = self.gateway.jvm.mff.agents.astarPlanningDynamic.Agent()

        return game.runGame(agent, '\n'.join(level), 30, 0, False, 4000, 2.0)
