import typing
from typing import Generator

from permutation import PermutationMethods
from utils import left_circular_shift

if typing.TYPE_CHECKING:
    from des import DES

class KeyMethods:
    def generate_keyring(self: 'DES') -> tuple[int, ...]:
        """각 Round에 적용할 key들을 하나의 tuple로 묶어서 반환하는 메서드."""
        # Permuted Choice 1을 initial key에 적용
        initially_permuted_key = PermutationMethods.permuted_choice1(self.key)

        # key를 상위 28bit와 하위 28bit로 분리
        left = initially_permuted_key >> 28
        right = initially_permuted_key & ((1 << 28) - 1)

        keyring:list[int] = [] # 각 round에 적용할 key 목록
        # generate_shifted_keys 제너레이터에서 각 단계마다 shift된 left와 right를 하나씩 받아서 keyring에 추가한 다음,
        # keyring을 tuple로 타입 변환해서 반환.
        for shifted_left, shifted_right in KeyMethods.generate_shifted_keys(left, right):
            keyring.append(PermutationMethods.permuted_choice2(shifted_left << 28 | shifted_right))
        return tuple(keyring)

    @staticmethod
    def generate_shifted_keys(left: int, right: int) -> Generator[tuple[int, int]]:
        """
        각 Round에 적용할 shift된 key를 생성하는 Generator를 반환하는 메서드.
        key: 56-bit int
        """
        for round_number in range(16):
            left = left_circular_shift(left, 1, 28)
            right = left_circular_shift(right, 1, 28)
            yield left, right
