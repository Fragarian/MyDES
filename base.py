"""
암호화 모듈의 기본 동작을 담당하는 모듈.
"""
import typing
from typing import Union

from permutation import PermutationMethods
from round import RoundMethods
from utils import split_half
from block import BlockMethods

if typing.TYPE_CHECKING:
    from des import DES

def format_blocks(blocks: list[Union[int, tuple[int, int]]]) -> str:
    if blocks and isinstance(blocks, list):
        if isinstance(blocks[0], int):
            return "-" * (2 + 20 * len(blocks)) + '\n|| '+' || '.join(map(lambda b: f"{b:016x}", blocks))+' ||\n' + "-" * (2 + 20 * len(blocks))
        elif isinstance(blocks[0], tuple):
            return "-" * (2 + 23 * len(blocks)) + '\n|| '+' || '.join(map(lambda b: f"{b[0]:08x} | {b[1]:08x}", blocks))+' ||\n'  + "-" * (2 + 23 * len(blocks))


class BaseMethods:
    def encrypt(self: 'DES',
                plaintext:bytes,
                ) -> bytes:

        # 0. split into cipher blocks
        blocks = list(map(lambda block: int.from_bytes(block, 'big'), BlockMethods.split(plaintext)))
        if self.debug_mode:
            print("***** Encryption *****")
            print(f"Plaintext: {plaintext}")
            print(f"Plaintext Integer Value:\n{format_blocks(blocks)}")

        # 1. Initial Permutation
        blocks = list(map(lambda block: PermutationMethods.initial_permutation(block), blocks))
        if self.debug_mode:
            print("After Initial Permutation:")
            print(format_blocks(blocks))
        # 1-1. 상하위 32비트를 각각 left와 right로 분리
        blocks = list(map(lambda block: split_half(block, bit_size=64), blocks))
        if self.debug_mode:
            print("After Split:")
            print(format_blocks(blocks))

        # 2. 라운드 15회 순회
        for i in range(16):
            if i < 15:
                blocks = list(map(lambda block: RoundMethods.round(block[0], block[1], self.keyring[i]), blocks))

            # 2-1. 마지막 16라운드에서는 bit-swap 생략
            else:
                blocks = list(map(lambda block: RoundMethods.round(block[0], block[1], self.keyring[i])[::-1], blocks))

            if self.debug_mode:
                print(f"Round {i+1}")
                print(format_blocks(blocks))


        blocks = list(map(lambda block: (block[0] << 32) | block[1],  blocks))
        if self.debug_mode:
            print("After Merge:")
            print(format_blocks(blocks))

        # 3. INVERSE Initial Permutation
        blocks = list(map(lambda block: PermutationMethods.initial_permutation(block, inverse=True), blocks))
        if self.debug_mode:
            print(f"After Inverse Initial Permutation:\n{format_blocks(blocks)}")

        # 4. merge cipher blocks
        encrypted = b''.join(map(lambda block: block.to_bytes(length=8, byteorder='big'), blocks))

        return encrypted

    def decrypt(self: 'DES',
                ciphertext:bytes,
                ) -> bytes:

        # 0. split into cipher blocks
        blocks = list(map(lambda block: int.from_bytes(block, 'big'), BlockMethods.split(ciphertext)))
        if self.debug_mode:
            print("***** Decryption *****")
            print(f"ciphertext: {ciphertext}")
            print(f"Plaintext Integer Value:\n{format_blocks(blocks)}")

        # 1. Initial Permutation
        blocks = list(map(lambda block: PermutationMethods.initial_permutation(block), blocks))
        if self.debug_mode:
            print("After Initial Permutation:")
            print(format_blocks(blocks))
        # 1-1. 상하위 32비트를 각각 left와 right로 분리
        blocks = list(map(lambda block: split_half(block, bit_size=64), blocks))
        if self.debug_mode:
            print("After Split:")
            print(format_blocks(blocks))

        # 2. 라운드 15회 순회
        for i in range(15, -1, -1):
            if i > 0:
                blocks = list(map(lambda block: RoundMethods.round(block[0], block[1], self.keyring[i]), blocks))

            # 2-1. 마지막 16라운드에서는 bit-swap 생략
            else:
                blocks = list(map(lambda block: RoundMethods.round(block[0], block[1], self.keyring[i])[::-1], blocks))

            if self.debug_mode:
                print(f"Round {i+1}")
                print(format_blocks(blocks))


        blocks = list(map(lambda block: (block[0] << 32) | block[1],  blocks))
        if self.debug_mode:
            print("After Merge:")
            print(format_blocks(blocks))

        # 3. INVERSE Initial Permutation
        blocks = list(map(lambda block: PermutationMethods.initial_permutation(block, inverse=True), blocks))
        if self.debug_mode:
            print(f"After Inverse Initial Permutation:\n{format_blocks(blocks)}")

        # 4. merge cipher blocks
        decrypted = b''.join(map(lambda block: block.to_bytes(length=8, byteorder='big'), blocks))

        return decrypted