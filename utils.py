def left_circular_shift(val: int, n: int, bit_size: int) -> int:
    n %= bit_size
    return ((val << n) | (val >> (bit_size - n))) & ((1 << bit_size) - 1) # 비트 수를 초과하지 않도록 마스킹

def right_circular_shift(val: int, n: int, bit_size: int) -> int:
    n %= bit_size
    return ((val >> n) | (val << (bit_size - n))) & ((1 << bit_size) - 1)

def bit32_swap(val: int):
    return left_circular_shift(val, n=32, bit_size=64)

