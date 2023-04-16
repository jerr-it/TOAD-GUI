
class Metric:
    def pre_hook(self):
        raise NotImplementedError

    def post_hook(
            self,
            original_level: list[str],
            generated_level: list[str],
            fixed_level: list[str],
    ) -> object:
        raise NotImplementedError
