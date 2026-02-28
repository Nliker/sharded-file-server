from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib
import os
from dotenv import load_dotenv

ENV = os.getenv("ENV", "development")

load_dotenv(f".env.{ENV}")


def derive_key_and_seed(password: str, unique_id: str) -> tuple[bytes, bytes]:
    salt = hashlib.sha256(f"salt:{unique_id}".encode()).digest()

    KEY_LEN = int(os.getenv("KEY_LEN"))
    SEED_LEN = int(os.getenv("SEED_LEN"))
    ITERATIONS = int(os.getenv("ITERATIONS"))

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LEN + SEED_LEN,
        salt=salt,
        iterations=ITERATIONS,
    )

    derived = kdf.derive(f"{password}:{unique_id}".encode())

    enc_key = derived[KEY_LEN:]
    seed = derived[:KEY_LEN]

    return enc_key, seed


def encrypt_bytes(enc_key: bytes, plaintext: bytes) -> bytes:
    aesgcm = AESGCM(enc_key)
    nonce = os.urandom(12)

    ciphertext = aesgcm.encrypt(
        nonce,
        plaintext,
        None,
    )

    return nonce + ciphertext
