import py4j.java_gateway


class Metric:
    def pre_hook(self):
        raise NotImplementedError

    def iter_hook(
        self,
        mario_result: py4j.java_gateway.JavaObject,
        fixed_level: list[str],
    ):
        raise NotImplementedError

    def post_hook(
        self,
        mario_result: py4j.java_gateway.JavaObject,
        original_level: list[str],
        generated_level: list[str],
        fixed_level: list[str],
    ) -> object:
        raise NotImplementedError
