import typing

if typing.TYPE_CHECKING:
    from des import DES


class RoundMethods:
    @staticmethod
    def round(_input: int,
              _scheduled_key: int
              ) -> int:
        # TODO: round 동작 구현 필요
        return _input