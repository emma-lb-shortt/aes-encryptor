# AES Encryption Demo

- Two files presented demonstrate two scripts that allow you to encrypt and decrypt a message from a text file into another text file:

## aes-encrypt.py

### How to run: 
- `python3 -m venv my_env`
- `source my_env/bin/activate`
- `pip install cryptography`
- `python3 aes-encrypt.py key=<filename> mode=ecb|cbc|gcm in=<filename> out=<filename> IV=<file containing IV>(optional) gmc_arg=<ASCII Value>`
- Note: no spaces between =

## aes-decrypt.py

### How to run: 
- `python3 -m venv my_env`
- `source my_env/bin/activate`
- `pip install cryptography`
- `python3 aes-decrypt.py key=<filename> mode=ecb|cbc|gcm in=<filename> out=<filename> IV=<file containing IV>(optional) gmc_arg=<ASCII Value>`
- Note: no spaces between =

## Modes:
- ECB
- CBC
- GCM
<img width="864" alt="Screenshot of code running" src="https://github.com/user-attachments/assets/b0a25d3a-c881-4b8d-96b2-9fc748424dbb">
