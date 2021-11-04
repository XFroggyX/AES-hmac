import sys
import argparse
from code_text import encrypt_text
from decode_text import decode_text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Encode/decode file')
    parser.add_argument('-code', dest="type_operation", type=str)
    parser.add_argument('-decode', dest="type_operation", type=str)
    parser.add_argument('-file', dest='save_file', default='text.txt', type=str)
    parser.add_argument('-key', dest='key', type=str)

    args = parser.parse_args()

    if sys.argv.count("-code"):
        encrypt_text(args.type_operation, args.save_file, args.key)
    elif sys.argv.count("-decode"):
        decode_text(args.type_operation, args.save_file, args.key)
    else:
        print(argparse.ArgumentTypeError("Operation type not specified"))

"""
-code mytext.txt -key pass.txt -file text.txt
-decode text.txt -key pass.txt -file dec.txt
"""