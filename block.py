"""
ECB의 블록 분할과 병합을 구현한 모듈.
"""

class BlockMethods:
    @staticmethod
    def split(plaintext: bytes) -> list[bytes]:
        assert len(plaintext) % 8 == 0, "This plaintext does not fit in ECB mode. Please pad this."
        result = []
        for i in range(0, len(plaintext), 8):
            result.append(plaintext[i:i+8])
        return result

    @staticmethod
    def merge(blocks: list[bytes]) -> bytes:
        return b''.join(blocks)