class Patcher:
    def patch(
            self,
            level_file: str,
            original_level: list[str],
            level: list[str],  # Level formatted as a list of strings row-wise
            broken_range: tuple[tuple[int, int], tuple[int, int]]  # (x_range, y_range)
    ) -> list[str]:
        raise NotImplementedError
