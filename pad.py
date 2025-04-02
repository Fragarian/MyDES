"""
패딩/언패딩이 구현된 모듈.
"""

class PadMethods:
    @staticmethod
    def pad(plaintext: bytes) -> bytes:
        pad_amount = (8 - (len(plaintext) % 8))
        return plaintext + pad_amount.to_bytes(1, 'big') * pad_amount

    @staticmethod
    def unpad(decrypted: bytes) -> bytes:
        pad_amount = decrypted[-1]
        return decrypted[:-pad_amount]
