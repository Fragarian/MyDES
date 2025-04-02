"""
기초적인 유틸 함수가 구현된 모듈.
"""

def left_circular_shift(val: int, n: int, bit_size: int) -> int:
    n %= bit_size
    return ((val << n) | (val >> (bit_size - n))) & ((1 << bit_size) - 1) # 비트 수를 초과하지 않도록 마스킹

def right_circular_shift(val: int, n: int, bit_size: int) -> int:
    n %= bit_size
    return ((val >> n) | (val << (bit_size - n))) & ((1 << bit_size) - 1)

def split_half(val:int, bit_size: int) -> tuple[int, int]:
    assert bit_size % 2 == 0, "split_half requires even number for bit size." # bit size로는 홀수가 입력될 수 없음.
    return val >> (bit_size//2), val & ((1 << (bit_size//2)) - 1)
