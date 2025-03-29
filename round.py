import typing

from permutation import PermutationMethods
from utils import split_half

if typing.TYPE_CHECKING:
    from des import DES


class RoundMethods:
    @staticmethod
    def round(left: int,
              right: int,
              _scheduled_subkey: int
              ) -> tuple[int, int]:
        """이전 단계의 중간 메세지(64비트)와 schedule 된 subkey를 사용하여 현재 단계의 메세지를 생성하는 메서드."""
        # 오른쪽 32비트는 왼쪽에 그대로 대입,
        # 왼쪽 32비트는 scheduled된 subkey와 함께 F function에 입력한 반환값을 오른쪽에 대입해서 Round 종료
        return right, left ^ RoundMethods.f(right, _scheduled_subkey)

    @staticmethod
    def f(_input: int,
          _scheduled_subkey: int
          ) -> int:
        """
        F function을 수행하고 결과를 반환하는 메서드.
        :parameter
            _input: int / 입력값. 32비트 정수.
            _scheduled_subkey: int / 스케줄된 키. 48비트 정수.
        """
        value = PermutationMethods.e_permutation(_input) ^ _scheduled_subkey # E-perm한 결과를 스케줄된 키와 XOR
        value = PermutationMethods.s_permutation(value) # 값을 S-perm
        return PermutationMethods.p_box(value) # 값을 P-box로 치환해서 최종 결과 반환
