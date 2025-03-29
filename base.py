import typing
from permutation import PermutationMethods
from round import RoundMethods
from utils import split_half

if typing.TYPE_CHECKING:
    from des import DES

class BaseMethods:
    def encrypt(self: 'DES',
                plaintext:bytes,
                ) -> bytes:

        val = int.from_bytes(plaintext, 'big')
        if self.debug_mode:
            print("-" * 40)
            print("Encryption")
            print("-" * 40)
            print(f"Plaintext: {plaintext}")
            print(f"Plaintext Integer Value: {val:016x}")
        # 1. Initial Permutation
        val = PermutationMethods.initial_permutation(val)
        if self.debug_mode:
            print("-"*20)
            print("After Initial Permutation")
            print("-"*20)
            print(f"Value: {val:016x}")
        # 1-1. 상하위 32비트를 각각 left와 right로 분리
        left, right = split_half(val, bit_size=64)
        if self.debug_mode:
            print(f"Left: {left:08x}, Right: {right:08x}")

        # 2. 라운드 15회 순회
        for i in range(16):
            left, right = RoundMethods.round(left, right, self.keyring[i])

            # 2-1. 마지막 16라운드에서는 bit-swap 생략
            if i == 15:
                left, right = right, left

            if self.debug_mode:
                print("-"*20)
                print(f"Round {i+1}")
                print("-"*20)
                print(f"Left: {left:08x}, Right: {right:08x}")

        val = (left << 32) | right
        if self.debug_mode:
            print(f"Value: {val:016x}")

        # 3. INVERSE Initial Permutation
        val = PermutationMethods.initial_permutation(val, inverse=True)
        if self.debug_mode:
            print("-"*20)
            print("After Inverse Initial Permutation")
            print("-"*20)
            print(f"Value: {val:016x}")

        return val.to_bytes(length=8, byteorder='big')

    def decrypt(self: 'DES',
                ciphertext:bytes,
                ) -> bytes:
        # 1. Initial Permutation
        val = PermutationMethods.initial_permutation(int.from_bytes(ciphertext))
        # 1-1. 상하위 32비트를 각각 left와 right로 분리
        left, right = split_half(val, bit_size=64)
        if self.debug_mode:
            print("-" * 40)
            print("Decryption")
            print("-" * 40)
            print(f"Ciphertext: {ciphertext}")
            print(f"Ciphertext Integer Value: {val:016x}")
            print("-"*20)
            print("After Inverse Initial Permutation")
            print("-"*20)
            print(f"Value: {val:016x}")

        # 2. 라운드 15회 순회
        for i in range(15, -1, -1):
            left, right = RoundMethods.round(left, right, self.keyring[i])

            # 2-1. 마지막 16라운드에서는 bit-swap 생략
            if i == 0:
                left, right = right, left

            if self.debug_mode:
                print("-"*20)
                print(f"Round {i+1}")
                print("-"*20)
                print(f"Left: {left:08x}, Right: {right:08x}")

        val = (left << 32) | right
        if self.debug_mode:
            print(f"Value: {val:016x}")

        # 3. INVERSE Initial Permutation
        val = PermutationMethods.initial_permutation(val, inverse=True)
        if self.debug_mode:
            print("-"*20)
            print("After Inverse Initial Permutation")
            print("-"*20)
            print(f"Value: {val:016x}")

        return val.to_bytes(length=8, byteorder='big')