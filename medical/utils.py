"""
Encryption utilities for the Coruscant Health Administration.

Uses Python standard library only (no external dependencies):
- PBKDF2-HMAC-SHA256 for key derivation (NIST SP 800-132 compliant)
- Counter-mode stream cipher using HMAC-SHA256 as PRF
- HMAC-SHA256 Encrypt-then-MAC for authenticated encryption

This provides confidentiality + integrity + authenticity for stored documents.
"""

import hashlib
import hmac
import os
import struct
from django.conf import settings


# ── Constants ──────────────────────────────────────────────────────
SALT_SIZE = 16          # 128-bit salt
IV_SIZE = 16            # 128-bit initialization vector
HMAC_SIZE = 32          # 256-bit HMAC tag
KEY_ITERATIONS = 260000  # OWASP 2023 recommendation for PBKDF2-SHA256


def _get_secret_key():
    """
    Return the encryption password. Uses FILE_ENCRYPTION_KEY from settings,
    falling back to Django's SECRET_KEY.
    """
    return getattr(settings, 'FILE_ENCRYPTION_KEY', settings.SECRET_KEY).encode()


def _derive_key(password, salt):
    """Derive a 256-bit key from a password and salt using PBKDF2."""
    return hashlib.pbkdf2_hmac(
        'sha256', password, salt, KEY_ITERATIONS, dklen=32
    )


def _generate_keystream(key, iv, length):
    """
    Generate a pseudo-random keystream in counter mode.
    Each block is HMAC-SHA256(key, iv || counter), giving 32 bytes per block.
    """
    keystream = b''
    counter = 0
    while len(keystream) < length:
        block_input = iv + struct.pack('>Q', counter)
        block = hmac.new(key, block_input, hashlib.sha256).digest()
        keystream += block
        counter += 1
    return keystream[:length]


def encrypt_data(plaintext_bytes):
    """
    Encrypt raw bytes.  Returns:  salt(16) || iv(16) || mac(32) || ciphertext
    """
    password = _get_secret_key()
    salt = os.urandom(SALT_SIZE)
    iv = os.urandom(IV_SIZE)
    key = _derive_key(password, salt)

    # XOR plaintext with keystream
    keystream = _generate_keystream(key, iv, len(plaintext_bytes))
    ciphertext = bytes(a ^ b for a, b in zip(plaintext_bytes, keystream))

    # Encrypt-then-MAC
    mac = hmac.new(key, salt + iv + ciphertext, hashlib.sha256).digest()

    return salt + iv + mac + ciphertext


def decrypt_data(encrypted_bytes):
    """
    Decrypt data produced by encrypt_data().
    Raises ValueError if the HMAC check fails (tampered/wrong key).
    """
    password = _get_secret_key()

    # Parse header
    offset = 0
    salt = encrypted_bytes[offset:offset + SALT_SIZE];       offset += SALT_SIZE
    iv   = encrypted_bytes[offset:offset + IV_SIZE];          offset += IV_SIZE
    mac  = encrypted_bytes[offset:offset + HMAC_SIZE];        offset += HMAC_SIZE
    ciphertext = encrypted_bytes[offset:]

    key = _derive_key(password, salt)

    # Verify integrity before decrypting
    expected_mac = hmac.new(key, salt + iv + ciphertext, hashlib.sha256).digest()
    if not hmac.compare_digest(mac, expected_mac):
        raise ValueError("Decryption failed: data integrity check failed (wrong key or tampered data)")

    # Decrypt
    keystream = _generate_keystream(key, iv, len(ciphertext))
    plaintext = bytes(a ^ b for a, b in zip(ciphertext, keystream))

    return plaintext
