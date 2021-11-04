import os
from hashlib import sha256, pbkdf2_hmac
import hmac
from Cryptodome import Random
from Cryptodome.Cipher import AES


# генерция соли
def gen_salt() -> bytes:
    return os.urandom(32)


# возвращает весь текст из файла
def get_str_from_file(file_name) -> str:
    with open(file_name) as file:
        text = file.read()
    return text


# хеш
def h_func_sha256(password_file, salt) -> bytes:
    password = get_str_from_file(password_file)
    key = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000, dklen=32)
    return key


# функция для кодирования текста
def encrypt(text, key, iv) -> tuple:
    # raw = _pad(text)
    cipher = AES.new(key, AES.MODE_CFB, iv)  # config
    encrypted_data = cipher.encrypt(text.encode())
    iv_data = iv + encrypted_data
    sig = hmac.new(key, iv_data, sha256).digest()
    return encrypted_data, sig


# запись в бинарный фаил
def writing_binary_file(file_name, text):
    with open(file_name, "wb") as file:
        file.write(text)


# добавляем не значимые нули к вектору
def vector_expansion(iv):
    list_iv = list(iv)
    while len(list_iv) < 32:
        list_iv.insert(0, 0)
    return bytes(list_iv)


# main func
def encrypt_text(text_file_name, code_file_name, password_file):
    salt = gen_salt()
    key = h_func_sha256(password_file, salt)

    iv = Random.new().read(AES.block_size)

    text = get_str_from_file(text_file_name)
    encrypt_txt, mac = encrypt(text, key, iv)
    encrypt_info = salt + mac + vector_expansion(iv)

    writing_binary_file(code_file_name, encrypt_info + encrypt_txt)
    return encrypt_info + encrypt_txt


if __name__ == "__main__":
    print(encrypt_text("text.txt", "crypt.bin", "pass.txt"))

