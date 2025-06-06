"""
permutation 기능을 구현한 모듈.
"""

import typing
from typing import Sequence

if typing.TYPE_CHECKING:
    from des import DES


class PermutationMethods:
    IP = (
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17,  9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7,
    ) # 64bit input, 64bit output
    IP_INVERSE = (
        40,  8, 48, 16, 56, 24, 64, 32,
        39,  7, 47, 15, 55, 23, 63, 31,
        38,  6, 46, 14, 54, 22, 62, 30,
        37,  5, 45, 13, 53, 21, 61, 29,
        36,  4, 44, 12, 52, 20, 60, 28,
        35,  3, 43, 11, 51, 19, 59, 27,
        34,  2, 42, 10, 50, 18, 58, 26,
        33,  1, 41,  9, 49, 17, 57, 25,
    ) # 64bit input, 64bit output
    E_TABLE = (
        32,  1,  2,  3,  4,  5,
         4,  5,  6,  7,  8,  9,
         8,  9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32,  1,
    ) # 32bit input, 48bit output

    S_BOX = [
        (
            14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,
             0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,
             4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0,
            15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13
        ), # S1
        (
            15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,
             3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,
             0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15,
            13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9
        ), # S2
        (
            10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,
            13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,
            13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,
             1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12
        ), # S3
        (
             7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15,
            13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9,
            10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,
             3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14
        ), # S4
        (
             2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9,
            14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6,
             4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14,
            11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3
        ), # S5
        (
            12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,
            10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,
             9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6,
             4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13,
        ), # S6
        (
             4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,
            13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,
             1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,
             6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12
        ), # S7
        (
            13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,
             1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,
             7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,
             2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11
        ), # S8
    ] # 6bit input, 4bit output

    P_BOX = (
        16,  7, 20, 21,
        29, 12, 28, 17,
         1, 15, 23, 26,
         5, 18, 31, 10,
         2,  8, 24, 14,
        32, 27,  3,  9,
        19, 13, 30,  6,
        22, 11,  4, 25,
    ) # 32bit input, 48bit output

    PC_1_BOX = (
        57, 49, 41, 33, 25, 17,  9,
         1, 58, 50, 42, 34, 26, 18,
        10,  2, 59, 51, 43, 35, 27,
        19, 11,  3, 60, 52, 44, 36, # C(상위 28비트)의 치환 방법

        63, 55, 47, 39, 31, 23, 15,
         7, 62, 54, 46, 38, 30, 22,
        14,  6, 61, 53, 45, 37, 29,
        21, 13,  5, 28, 20, 12,  4, # D(하위 28비트)의 치환 방법
    ) # 64bit input, 28bit+28bit output

    PC_2_BOX = (
        14, 17, 11, 24,  1,  5,
         3, 28, 15,  6, 21, 10,
        23, 19, 12,  4, 26,  8,
        16,  7, 27, 20, 13,  2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32,
    ) # 56-bit input, 48-bit output

    @staticmethod
    def initial_permutation(_input: int,
                            inverse: bool=False,
                            ) -> int:
        if not inverse:
            return PermutationMethods.basic_permutation(_input, PermutationMethods.IP, input_bit_size=64)
        else:
            return PermutationMethods.basic_permutation(_input, PermutationMethods.IP_INVERSE, input_bit_size=64)

    @staticmethod
    def e_permutation(_input: int) -> int:
        """E permutation 치환 결과를 구하는 메서드."""
        return PermutationMethods.basic_permutation(_input, PermutationMethods.E_TABLE, input_bit_size=32)

    @staticmethod
    def s_permutation(_input: int) -> int:
        input_mask = (1 << 6) - 1
        result = 0
        for box_number in range(8):
            # "input의 6비트를 s-box로 치환한 4비트 결과값"을 result의 하위 4비트에 추가
            result = (result << 4) | PermutationMethods.s_box((_input >> (6 * (7-box_number))) & input_mask, box_number)

        return result

    @staticmethod
    def s_box(_input: int, box_number: int) -> int:
        """S-box 치환 결과를 구하는 메서드. box_number로 S1~S8을 지정한다."""
        outer_bits = (_input >> 5 << 1) | (_input & 1) # outer bits 추출
        inner_bits = _input >> 1 & ((1 << 4) - 1) # inner bits 추출

        # 입력 number에 해당하는 S-box에서 input에 해당하는 값 반환
        return PermutationMethods.S_BOX[box_number][outer_bits << 4 | inner_bits]

    @staticmethod
    def p_box(_input):
        """P-Box 치환 결과를 구하는 메서드."""
        return PermutationMethods.basic_permutation(_input, PermutationMethods.P_BOX, input_bit_size=32)


    @staticmethod
    def permuted_choice1(key: int) -> tuple[int, int]:
        """Permuted choice 1 치환 결과를 구하는 메서드."""
        # c: 치환 결과의 상위 28비트, d: 치환 결과의 하위 28비트. 즉, 전체 치환 결과는 56비트이다.
        c = PermutationMethods.basic_permutation(key, PermutationMethods.PC_1_BOX[:28], input_bit_size=64)
        d = PermutationMethods.basic_permutation(key, PermutationMethods.PC_1_BOX[28:], input_bit_size=64)

        return c, d

    @staticmethod
    def permuted_choice2(_input: int) -> int:
        """Permuted choice 2 치환 결과를 구하는 메서드."""
        return PermutationMethods.basic_permutation(_input, PermutationMethods.PC_2_BOX, input_bit_size=56)

    @staticmethod
    def basic_permutation(_input: int, box: Sequence[int], input_bit_size: int) -> int:
        result = 0
        for bit_position in box:
            # box의 i번째 값은, result의 i번째 비트에 들어가야 할 비트의 input에서의 위치를 뜻한다.
            # 즉, 반복문에서 현재 순회중인 box 값 위치에 있는 bit를 구해서 추가한다.
            # box 의 값은 왼쪽(최상위 비트)에서부터의 1-start index이므로,
            # 최하위 비트(lsb)와의 거리를 구하려면 input의 bit size에서 빼야 한다.
            result = (result << 1) | (_input >> (input_bit_size - bit_position)) & 1
        return result



