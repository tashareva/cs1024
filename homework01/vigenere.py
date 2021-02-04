def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    ind = 0
    for i in plaintext:
        if i.isupper():
            ciphertext += chr(
                (ord(i) - ord("A") + (ord(keyword[ind % len(keyword)]) - ord("A"))) % 26 + ord("A")
            )
        elif i.islower():
            ciphertext += chr(
                (ord(i) - ord("a") + (ord(keyword[ind % len(keyword)]) - ord("a"))) % 26 + ord("a")
            )
        else:
            ciphertext += i
        ind += 1

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    ind = 0
    for i in ciphertext:
        if i.isupper():
            plaintext += chr(
                (ord(i) - ord("A") - (ord(keyword[ind % len(keyword)]) - ord("A"))) % 26 + ord("A")
            )
        elif i.islower():
            plaintext += chr(
                (ord(i) - ord("a") - (ord(keyword[ind % len(keyword)]) - ord("a"))) % 26 + ord("a")
            )
        else:
            plaintext += i
        ind += 1

    return plaintext
