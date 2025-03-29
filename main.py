import timeit
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

from des import DES as MyDES

debug_mode = True

if __name__ == '__main__':
    # key를 bytes array로 선언
    key = 0x133457799BBCDFF1.to_bytes(8, byteorder='big')
    
    ### 직접 구현한 DES ###

    my_cipher = MyDES(debug_mode=debug_mode)

    # 1. 원문(plaintext)
    plaintext:bytes = b"ABCDEFGH"

    # 2. 암호화 -> 암호문(ciphertext)
    ciphertext:bytes = my_cipher.encrypt(plaintext)

    # 2-1. 암호화를 100번 실행하고 시간을 timeit으로 측정
    run_count = 100
    encryption_time = timeit.timeit(lambda: my_cipher.encrypt(plaintext, debug_mode=False), number=run_count)

    # 3. 복호화 -> 원문(plaintext) 이자 복호문(decrypted ciphertext)
    decrypted_ciphertext:bytes = my_cipher.decrypt(ciphertext)

    # 3-1. 복호화를 100번 실행하고 시간을 timeit으로 측정
    run_count = 100
    decryption_time = timeit.timeit(lambda: my_cipher.decrypt(ciphertext, debug_mode=False), number=run_count)

    # 4. 결과 출력
    print("-"*40)
    print("By custom implemented DES")
    print("-" * 40)
    print(f"Plaintext:\t\t\t\t{plaintext}")
    print(f"Encrypted Ciphertext:\t\t{hex(int.from_bytes(ciphertext, byteorder='big'))}")
    print(f"Execution Time (Encryption, 100 runs): {encryption_time}")
    print(f"Decrypted Plaintext:\t\t\t\t{decrypted_ciphertext}")
    print(f"Execution Time (Decryption, 100 runs): {decryption_time}")


    ### pycryptodome 상용 패키지의 DES ###

    cipher = DES.new(key, DES.MODE_ECB)

    # 1. 원문(plaintext)
    plaintext:bytes = b"ABCDEFGH"

    # 암호문의 길이가 정확히 8바이트로 나누어 떨어져서 패딩이 필요 없다고 하더라도,
    # 보안성과 패딩의 정확한 인식을 위해서 항상 8바이트의 패딩을 추가한다고 한다.
    # 그러나 암호화된 ciphertext를 확인할 때 불편하고, 성능 비교 시 상용 모듈만 16바이트를 암호화하는 것은 부정확하므로,
    # 암호문의 길이가 8의 배수일 때는 패딩을 생략하는 것으로 통일한다.
    skip_padding = plaintext and len(plaintext) % 8 == 0
    padded_plaintext = plaintext if skip_padding else pad(plaintext, DES.block_size)

    # 2. 암호화 -> 암호문(ciphertext)
    ciphertext:bytes = cipher.encrypt(padded_plaintext)

    # 2-1. 암호화를 100번 실행하고 시간을 timeit으로 측정
    run_count = 100
    encryption_time = timeit.timeit(lambda: cipher.encrypt(padded_plaintext), number=run_count)

    # 3. 복호화 -> 원문(plaintext)이자 복호문(decrypted ciphertext)
    decrypted_ciphertext:bytes = cipher.decrypt(ciphertext)
    # 만약 plaintext에서 패딩을 추가하지 않았다면, 복호문에서 패드 제거도 하지 않는다.
    unpadded_ciphertext:bytes = decrypted_ciphertext if skip_padding else unpad(decrypted_ciphertext, DES.block_size)

    # 3-1. 복호화를 100번 실행하고 시간을 timeit으로 측정
    run_count = 100
    decryption_time = timeit.timeit(lambda: cipher.decrypt(ciphertext), number=run_count)


    # 4. 결과 출력
    print("-" * 40)
    print("By reference library DES")
    print("-" * 40)
    print(f"Plaintext:\t\t\t\t{plaintext}")
    print(f"Encrypted Ciphertext:\t\t{hex(int.from_bytes(ciphertext, byteorder='big'))}")
    print(f"Execution Time (Encryption, 100 runs): {encryption_time}")
    print(f"Decrypted Plaintext:\t\t\t\t{unpadded_ciphertext}")
    print(f"Execution Time (Decryption, 100 runs): {decryption_time}")
