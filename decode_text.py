import sys
from hashlib import sha256

from code_text import h_func_sha256
import hmac
from Cryptodome.Cipher import AES


# возвращает весь бинарный текст из файла
def reading_binary_file(file_name):
    with open(file_name, 'rb') as file:
        text = file.read()
    return text


# возвращает кусок бинарной строки
def get_bin_slice(byte_line, slice_start, slice_end=None):
    slice_list = []
    try:
        for i in range(slice_start, slice_end):
            slice_list.append(byte_line[i])
    except IndexError:
        return slice_list
    return slice_list


# удаляем не значимые нули из вектора
def clearing_vector(iv):
    while iv[0] == 0:
        del iv[0]
    return iv


# проверка hmac
def hmac_check(gen_hmac, hmac_from_file):
    if len(gen_hmac) != len(hmac_from_file):
        print("invalid MAC size")
        return False

    if gen_hmac == hmac_from_file:
        return True
    return False


# запись в фаил
def writing_file(file_name, text):
    with open(file_name, "w") as file:
        file.write(text)


# main func
def decode_text(code_file_name, text_file_name, password_file):
    encrypt_text_from_file = reading_binary_file(code_file_name)

    salt = bytes(get_bin_slice(encrypt_text_from_file, 0, 32))
    key = h_func_sha256(password_file, salt)

    iv = get_bin_slice(encrypt_text_from_file, 64, 96)
    iv = bytes(clearing_vector(iv))

    encrypt_text = bytes(get_bin_slice(encrypt_text_from_file, 96, len(encrypt_text_from_file)))
    iv_data = iv + encrypt_text

    mac = bytes(get_bin_slice(encrypt_text_from_file, 32, 64))

    check = hmac_check(hmac.new(key, iv_data, sha256).digest(), mac)
    if not check:
        sys.exit("Hmac does not match")

    cipher = AES.new(key, AES.MODE_CFB, iv)
    text = cipher.decrypt(encrypt_text).decode()
    writing_file(text_file_name, text)
    return text


if __name__ == "__main__":
    print(decode_text("crypt.bin", "mytext.txt", "pass.txt"))
