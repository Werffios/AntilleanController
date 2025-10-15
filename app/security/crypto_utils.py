import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from dotenv import load_dotenv

load_dotenv()

_ENC_KEY_ENV = os.getenv("ENCRYPTION_KEY", "")
_ENFORCE = os.getenv("ENFORCE_ENCRYPTED_INPUT", "false").lower() == "true"


def _decode_key() -> bytes:
    if not _ENC_KEY_ENV:
        raise ValueError("ENCRYPTION_KEY no está configurada.")
    try:
        key = base64.urlsafe_b64decode(_ENC_KEY_ENV)
    except Exception:
        raise ValueError("ENCRYPTION_KEY no es Base64 URL-safe válido.")

    if len(key) not in (16, 24, 32):
        raise ValueError("La clave decodificada debe tener 16, 24 o 32 bytes para AES.")
    return key


def encrypt_text(plaintext: str) -> str:
    key = _decode_key()

    if not isinstance(plaintext, str):
        plaintext = str(plaintext)

    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(plaintext.encode("utf-8"), AES.block_size)
    ciphertext = cipher.encrypt(padded)

    iv_hex = iv.hex()
    ciphertext_b64 = base64.b64encode(ciphertext).decode("utf-8")
    payload = f"{iv_hex}:{ciphertext_b64}".encode("utf-8")
    return base64.b64encode(payload).decode("utf-8")


def decrypt_text(encrypted_b64: str) -> str:
    key = None
    try:
        key = _decode_key()

        decoded_payload = base64.b64decode(encrypted_b64).decode('utf-8')

        iv_hex, ciphertext_b64 = decoded_payload.split(':')
        iv = bytes.fromhex(iv_hex)
        ciphertext = base64.b64decode(ciphertext_b64)

        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(ciphertext)

        decrypted = unpad(decrypted_padded, AES.block_size)

        return decrypted.decode('utf-8')

    except Exception:
        if not _ENFORCE:
            return encrypted_b64
        raise ValueError("Credencial encriptada inválida o clave incorrecta.")


def generate_encryption_key(num_bytes: int = 32) -> str:
    if num_bytes not in (16, 24, 32):
        raise ValueError("num_bytes debe ser 16, 24 o 32 para AES.")
    return base64.urlsafe_b64encode(os.urandom(num_bytes)).decode("utf-8")
