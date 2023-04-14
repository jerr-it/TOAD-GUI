
class Metric:
    def pre_hook(self):
        raise NotImplementedError

    def post_hook(self, fixed_level: list[str]) -> object:
        raise NotImplementedError
