from typing import Optional

class DES:
    """
    DES 알고리즘에 따라 Block Cipher Encryption을 수행하는 객체.
    """
    def __init__(self,
                 block_size:int=64,
                 key_size:int=64,
                 debug_mode:bool=False,
                 ) -> None:
        self.block_size = block_size
        self.key_size = key_size
        self.debug_mode = debug_mode

    def encrypt(self,
                plaintext,
                debug_mode:bool=True
                ) -> bytes:
        if self.debug_mode and debug_mode:
            print(f"Debug mode is activated!")
            print(f"Block size: {self.block_size}bit")
            print(f"Key size: {self.key_size}bit")
            print(f"Plaintext: {plaintext}")
        # TODO: 암호화 동작 구현 필요
        return plaintext

    def decrypt(self,
                ciphertext,
                debug_mode:bool=True
                ) -> bytes:
        if self.debug_mode and debug_mode:
            print(f"Debug mode is activated!")
            print(f"Block size: {self.block_size}bit")
            print(f"Key size: {self.key_size}bit")
            print(f"Ciphertext: {ciphertext}")
        # TODO: 복호화 동작 구현 필요
        return ciphertext