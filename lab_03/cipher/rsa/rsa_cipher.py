import rsa
import os
import base64

KEY_DIR = "cipher/rsa/keys"

if not os.path.exists(KEY_DIR):
    os.makedirs(KEY_DIR)


class RSACipher:
    def __init__(self):
        self.public_key_path = os.path.join(KEY_DIR, "publicKey.pem")
        self.private_key_path = os.path.join(KEY_DIR, "privateKey.pem")

    def generate_keys(self):
        """
        Tạo cặp khóa RSA 1024 bit
        """
        public_key, private_key = rsa.newkeys(1024)

        with open(self.public_key_path, "wb") as f:
            f.write(public_key.save_pkcs1("PEM"))

        with open(self.private_key_path, "wb") as f:
            f.write(private_key.save_pkcs1("PEM"))

        return True

    def load_keys(self):
        """
        Đọc khóa từ file
        """
        if not os.path.exists(self.public_key_path):
            raise FileNotFoundError("Public key không tồn tại")

        if not os.path.exists(self.private_key_path):
            raise FileNotFoundError("Private key không tồn tại")

        with open(self.public_key_path, "rb") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read())

        with open(self.private_key_path, "rb") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())

        return private_key, public_key

    def encrypt(self, message, public_key):
        """
        Mã hóa chuỗi và trả về Base64
        """
        encrypted = rsa.encrypt(
            message.encode("utf-8"),
            public_key
        )

        return base64.b64encode(encrypted).decode("utf-8")

    def decrypt(self, ciphertext, private_key):
        """
        Giải mã Base64
        """
        try:
            ciphertext = base64.b64decode(ciphertext)

            decrypted = rsa.decrypt(
                ciphertext,
                private_key
            )

            return decrypted.decode("utf-8")

        except Exception as e:
            return str(e)

    def sign(self, message, private_key):
        """
        Ký số bằng SHA-256
        """
        signature = rsa.sign(
            message.encode("utf-8"),
            private_key,
            "SHA-256"
        )

        return base64.b64encode(signature).decode("utf-8")

    def verify(self, message, signature, public_key):
        """
        Xác thực chữ ký
        """
        try:
            signature = base64.b64decode(signature)

            result = rsa.verify(
                message.encode("utf-8"),
                signature,
                public_key
            )

            return result == "SHA-256"

        except Exception:
            return False