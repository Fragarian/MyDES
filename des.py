"""
모든 기능을 상속한 완성된 암호화 모듈.
"""
from typing import Optional, Union
from base import BaseMethods
from round import RoundMethods
from key import KeyMethods

class DES(BaseMethods, RoundMethods, KeyMethods):
    """
    DES 알고리즘에 따라 Block Cipher Encryption을 수행하는 객체.
    """
    def __init__(self,
                 key:Union[bytes, int],
                 debug_mode:bool=False,
                 ) -> None:
        self.key = key
        self.debug_mode = debug_mode

        self.keyring:tuple[int, ...] = self.generate_keyring()

        if self.debug_mode:
            print(f"Debug mode is activated!")
            print("Keyring:")
        for idx in range(0, 16, 4):
            for subkey in self.keyring[idx:idx + 4]:
                print(hex(subkey), end=' ')
            print()