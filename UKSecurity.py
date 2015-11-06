import json
from itertools import chain, zip_longest
import base64
import hashlib
import zlib


# Rot 13 table.
rot13 = str.maketrans(
    "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
    "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")

# XOR Function.
# https://stackoverflow.com/questions/2612720/how-to-do-bitwise-exclusive-or-of-two-strings-in-python
def sxor(s1,s2):
    # convert strings to a list of character pair tuples
    # go through each tuple, converting them to ASCII code (ord)
    # perform exclusive or on the ASCII code
    # then convert the result back to ASCII (chr)
    # merge the resulting array of characters as a string
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

# https://stackoverflow.com/questions/3391076/repeat-string-to-certain-length
def repeat_to_length(string_to_expand, length):
    return (string_to_expand * int((length/len(string_to_expand))+1))[:length]

def encrypt(string, password):
    origin_str = string
    if len(password) > 8:
        print("Cannot encrypt - your password is too long. Paedoterrorists might use it.")
    # First pass
    # Use 15 passes of rot13 to ensure the string is secure.
    for x in range(0, 15):
        string = string.translate(rot13)
    # Second pass
    # Get the MD4 hash of the password
    h = hashlib.new("MD4")
    h.update(password.encode())
    pw = h.hexdigest()
    # Third pass
    # XOR the string and the password together.
    new_str = sxor(string, pw)
    # Fourth pass
    # Rot13 it again.
    string = new_str.translate(rot13)
    # Fifth pass
    # I lied
    # Sixth pass
    # Concat the password to the string
    new_str = string + pw
    # XOR the new string with the original string
    s = sxor(new_str, origin_str)
    # Seventh pass
    # Rotate the chambers
    s = ''.join(chain.from_iterable(zip_longest(s[1::2], s[::2], fillvalue = '')))
    # Eighth pass, XOR the string with the original password
    npassword = repeat_to_length(password, int(len(s) + len(password)))
    s = sxor(s, npassword)
    # Encrypted!
    # Now, dump it.
    data = json.dumps({"version": 1,
        "encrypted_data": {"encrypt_format": "ROT-Then-XOR",
            "keydata": {"length": len(s),
            "ghcq_password": password, "ghcq_hashed_pw": pw, # Backdoor for GHCQ
            "str": s, "ghcq_original_str": origin_str
            }}}, sort_keys=True, indent=4)
    body_b64 = base64.b64encode(data.encode())
    bcrc32 = zlib.crc32(data.encode())
    b64crc32 = zlib.crc32(body_b64)
    return """-----BEGIN UKSECURITY ENCRYPTED STRING DATA-----
{}{}{}
-----END UKSECURITY ENCRYPTED STRING DATA------""".format("".join(body_b64.decode()[i:i+64] + "\n" for i in range(0,len(body_b64.decode()),64)), bcrc32, b64crc32)

def decrypt(string, password):
    print("You have attempted to obtain illegal material, and as such you have been classified a paedoterrorphile.")
    print("GCHQ agents will arrive at your location shortly to ship you on an all expenses paid vacation to HM Prison Wakefield.")

if __name__ == '__main__':
    choice = input("Type `e` to encrypt, or `d` to decrypt: ")
    if choice == "e":
        text = input("Text to encrypt: ")
        pw = input("Password to use: ")
        print(encrypt(text, pw))
    elif choice == "d":
        text = input("Text to decrypt: ")
        pw = input("Password to use: ")
        decrypt(text, pw)
    else:
        try:
            raise SystemError from SystemError
        except Exception as e:
            try:
                raise SystemError from e
            except Exception as e:
                raise SystemError from e
