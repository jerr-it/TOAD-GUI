import py4j.java_gateway


class Patcher:
    def patch(
            self,
            original_level: list[str],
            level: list[str],  # Level formatted as a list of strings row-wise
            broken_range: tuple[tuple[int, int], tuple[int, int]],  # (x_range, y_range)
            generator_path: str = "",
            mario_result: py4j.java_gateway.JavaObject = None
    ) -> list[str]:
        raise NotImplementedError
