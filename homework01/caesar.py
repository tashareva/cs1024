import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    ciphertext = ""
    for i in plaintext:
        if i.isupper():
            code = (ord(i) - ord("A") + shift) % 26 + ord("A")
            sym = chr(code)
            ciphertext += sym
        elif i.islower():
            code = (ord(i) - ord("a") + shift) % 26 + ord("a")
            sym = chr(code)
            ciphertext += sym
        else:
            ciphertext += i
    return ciphertext
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for i in ciphertext:
        if i.isupper():
            if ord(i) - ord("A") < shift:
                code = 25 - ((shift - 1) - (ord(i) - ord("A"))) + ord("A")
            else:
                code = ord(i) - ord("A") - shift + ord("A")
            sym = chr(code)
            plaintext += sym
        elif i.islower():
            if ord(i) - ord("a") < shift:
                code = 25 - ((shift - 1) - (ord(i) - ord("a"))) + ord("a")
            else:
                code = ord(i) - ord("a") - shift + ord("a")
            sym = chr(code)
            plaintext += sym
        else:
            plaintext += i
    return plaintext


def caesar_breaker(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    >>> d = {"python", "java", "ruby"}
    >>> caesar_breaker("python", d)
    0
    >>> caesar_breaker("sbwkrq", d)
    3
    """
    best_shift = 0
    for i in dictionary:
        if ciphertext == i:
            return 0
        for shift in range(25):
            word = decrypt_caesar(ciphertext, shift)
            if word == i:
                return shift
    best_shift += shift
    return best_shift
