import typing

if typing.TYPE_CHECKING:
    from des import DES

class BaseMethods:
    def encrypt(self: 'DES',
                plaintext,
                debug_mode:bool=True
                ) -> bytes:
        if self.debug_mode and debug_mode:
            print(f"Debug mode is activated!")
            print(f"Block size: {self.block_size}bit")
            print(f"Key size: {self.key_size}bit")
            print(f"Plaintext: {plaintext}")
            print("Keyring:")
            for idx in range(0, 16, 4):
                for subkey in self.keyring[idx:idx+4]:
                    print(hex(subkey), end=' ')
                print()
        # TODO: 암호화 동작 구현 필요
        return plaintext

    def decrypt(self: 'DES',
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