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
                 block_size:int=64,
                 key_size:int=64,
                 debug_mode:bool=False,
                 ) -> None:
        self.key = key
        self.block_size = block_size
        self.key_size = key_size
        self.debug_mode = debug_mode

        self.keyring:tuple[int, ...] = self.generate_keyring()