import base64

class URLConverter:
    def __init__(self, url, mode, shift=13):
        self.url = url
        self.mode = mode
        self.shift = shift
        self.valid_modes = ['base64', 'plain', 'hex', 'binary', 'octal', 'caesar']

    def convert(self):
        if self.mode == 'b64':
            return self.base64_decode()
        elif self.mode == 'plain':
            return self.url
        elif self.mode == 'hex':
            return self.hex_decode()
        elif self.mode == 'bin':
            return self.binary_decode()
        elif self.mode == 'oct':
            return self.octal_decode()
        elif self.mode == 'csr':
            return self.caesar_decode()
        else:
            return f"error/convert_failed"

    def binary_decode(self):
        try:
            decoded_url = ''.join(chr(int(self.url[i:i+8], 2)) for i in range(0, len(self.url), 8))
            return decoded_url
        except Exception as e:
            return "error/invalid_binary_string"
        
    def octal_decode(self):
        try:
            decoded_url = ''.join(chr(int(self.url[i:i+3], 8)) for i in range(0, len(self.url), 3))
            return decoded_url
        except Exception as e:
            return "error/invalid_octal_string"

    def hex_decode(self):
        try:
            decoded_url = bytes.fromhex(self.url).decode('utf-8')
            return decoded_url
        except Exception as e:
            return "error/invalid_hex_string"

    def decode_base64url(self, base64url_string):
        padding = len(base64url_string) % 4
        if padding:
            base64url_string += "=" * (4 - padding)
        return base64.urlsafe_b64decode(base64url_string)

    def base64_decode(self):
        try:
            decoded_bytes = self.decode_base64url(self.url)
            decoded_url = decoded_bytes.decode('utf-8')
            return decoded_url
        except Exception as e:
            return "error/invalid_base64_string"
    
    def caesar_decode(self):
        try:
            decoded_url = ''.join(
                chr((ord(char) - self.shift - 97) % 26 + 97) if char.islower() else
                chr((ord(char) - self.shift - 65) % 26 + 65) if char.isupper() else char
                for char in self.url
            )
            return decoded_url
        except Exception as e:
            return "error/invalid_caesar_string"

# test2 = URLConverter('aGVsbG8gd29ybGQ', 'base64')
# print(test2.convert())  # Should print: hello world
# test3 = URLConverter('0110100001100101011011000110110001101111001000000111011101101111011100100110110001100100', 'binary')
# print(test3.convert()) # Should print: hello world
# test4 = URLConverter('68656c6c6f20776f726c64', 'hex')
# print(test4.convert())  # Should print: hello world
# test5 = URLConverter('150145154154157040167157162154144', 'octal')
# print(test5.convert())  # Should print: hello world
# test6 = URLConverter('khoor zruog', 'caesar', shift=3)
# print(test6.convert())  # Should print: hello world