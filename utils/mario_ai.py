import os

import py4j.java_gateway
from py4j.java_gateway import JavaGateway
from enum import Enum

# old: MARIO_AI_PATH = os.path.abspath(os.path.join(os.path.curdir, "Mario-AI-Framework/mario-1.0-SNAPSHOT.jar"))
MARIO_AI_PATH = os.path.abspath(os.path.join(os.path.curdir, "Mario-AI-Framework/mario_ai_revisited.jar"))


class AgentType(Enum):
    Human = 1
    AstarDynamicPlanning = 2


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

    def evaluate_level(
        self,
        level: list[str],
        agent: AgentType,
        visual: bool,
        speed: int,
        timeout: int
    ) -> py4j.java_gateway.JavaObject:
        match agent:
            case AgentType.Human:
                game = self.gateway.jvm.engine.core.MarioGame()
                agent = self.gateway.jvm.agents.human.Agent()

                return game.runGame(agent, '\n'.join(level), timeout, 0, visual, speed, 2.0)

            case AgentType.AstarDynamicPlanning:
                game = self.gateway.jvm.mff.agents.common.AgentMarioGame()
                agent = self.gateway.jvm.mff.agents.astarPlanningDynamic.Agent()

                return game.runGame(agent, '\n'.join(level), timeout, 0, visual, speed, 2.0)
