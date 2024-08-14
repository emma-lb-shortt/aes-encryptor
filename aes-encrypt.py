import sys
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# 
# Name: Emma Shortt
# Student Number: 1095620
# Program Name: aes-encrypt.py
# How to run: 
# python3 -m venv my_env
# source my_env/bin/activate
# pip install cryptography
# python3 aes-encrypt.py key=<filename> mode=ecb|cbc|gcm in=<filename> out=<filename> IV=<file containing IV>(optional) gmc_arg=<ASCII Value>
# Note: no spaces between =
# 

# Method Name: parse_input
# Functionality: Goes through the command line input and returns a dict or the input, values
def parse_input(argv):
    commands = []
    values = []
    for argument in argv:
        split_arguments = argument.split("=")
        if len(split_arguments) == 2:
            commands.append(split_arguments[0].lower())
            values.append(split_arguments[1])
    
    key_value_pairs = zip(commands, values)
    dict_arguments = dict(key_value_pairs)
    verify_input(dict_arguments)
    return (dict_arguments)

# Method Name: verify_input
# Functionality: Ensures that all parameters are there to execute a specific mode
def verify_input (dict_arguments):
    if "key" not in dict_arguments or "mode" not in dict_arguments or "in" not in dict_arguments or "out" not in dict_arguments:
        print ("USAGE: python3 aes-encrypt.py key=<filename> mode=ecb|cbc|gcm in=<filename> out=<filename> IV=<file containing IV>(optional) gmc_arg=<ASCII Value>")
        exit (-1)
    elif (dict_arguments["mode"] == "cbc" or dict_arguments["mode"] == "gcm") and "iv" not in dict_arguments:
        print ("Error - iv is necessary for cbc and gcm encryption")
        exit(-1)
    elif dict_arguments["mode"] == "gcm" and "gcm_arg" not in dict_arguments:
        print ("Error - gcm_arg is necessary for gcm encryption")
        exit(-1)

# Method Name: encrypt_ecb
# Functionality: Performs AES encryption in ECB mode
# Code from: https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/
def encrypt_ecb(key, input_value):
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(input_value)
    padded_data += padder.finalize()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    return ct

# Method Name: encrypt_cbc
# Functionality: Performs AES encryption in cbc mode
# Code from: https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/
def encrypt_cbc(key, input_value, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(input_value)
    padded_data += padder.finalize()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    return ct

# Method Name: encrypt_gcm
# Functionality: Performs AES encryption in gcm mode
# Code from: https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#cryptography.hazmat.primitives.ciphers.modes.GCM
def encrypt_gcm(key, input_value, iv, gcm_arg):
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
    encryptor = cipher.encryptor()
    
    encryptor.authenticate_additional_data(bytes(gcm_arg, "utf-8"))

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(input_value)
    padded_data += padder.finalize()
    ct = encryptor.update(padded_data) + encryptor.finalize()

    # save the tag to be used to decrypt
    tag_file = open("tag", "wb")
    tag_file.write(encryptor.tag)
    tag_file.close()

    return ct

def create_input(file_name):
    if os.path.exists(file_name) == False:
        print("Error - file (" + file_name + ") does not exist")
        exit(-1)
    fk = open(file_name, "rb")
    value = fk.read()
    fk.close()
    return value

def main():
    # Ensures correct number of arguements are entered
    if len(sys.argv) < 4:
        print ("USAGE: python3 aes-encrypt.py key=<filename> mode=ecb|cbc|gcm in=<filename> out=<filename> IV=<file containing IV>(optional) gmc_arg=<ASCII Value>")
        exit (-1)

    # parsing input
    dict_arguments = parse_input(sys.argv)

    # intializing necessary variables based on arguments
    key = create_input(dict_arguments["key"])
    mode = dict_arguments["mode"].lower()
    input_value = create_input(dict_arguments["in"])
    out_file = dict_arguments["out"]

    # Calling respective ecryption methods
    if (mode == "cbc"):
        iv_value = create_input(dict_arguments["iv"])
        cipher_text = encrypt_cbc(key, input_value, iv_value)
        fo = open(out_file, "wb")
        fo.write(cipher_text)
        fo.close()
    elif (mode == "ecb"):
        cipher_text = encrypt_ecb(key, input_value)
        fo = open(out_file, "wb")
        fo.write(cipher_text)
        fo.close()
    elif (mode == "gcm"):
        iv_value = create_input(dict_arguments["iv"])
        gcm_arg = dict_arguments["gcm_arg"]
        cipher_text = encrypt_gcm(key, input_value, iv_value, gcm_arg)
        fo = open(out_file, "wb")
        fo.write(cipher_text)
        fo.close()
    else:
        print ("Error - mode provided is not one of the options - please try again with ecb or cbc or gcm")
        exit(-1)
   
if __name__ == "__main__":
    main()
