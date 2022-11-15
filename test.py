'''def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


temp = text_to_bits('Привет')
print(temp)
print(text_from_bits(temp))
hexed = hex(int(temp))
print(hexed)
print(text_from_bits(str(int(hexed, 16))))'''


def encrypt(string):
    bits = bin(int.from_bytes(string.encode('utf-8', 'surrogatepass'), 'big'))[2:]
    return hex(int(bits.zfill(8 * ((len(bits) + 7) // 8))))


def decrypt(string):
    n = int(str(int(string, 16)), 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode('utf-8', 'surrogatepass') or '\0'

s = encrypt('Привет')
print(s)
print(decrypt(s))


