"""
Custom Django file storage that transparently encrypts files on save
and decrypts them on read.

Files stored on disk are fully encrypted — they cannot be opened
or read without the correct encryption key.
"""

import io
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from .utils import encrypt_data, decrypt_data


class EncryptedFileSystemStorage(FileSystemStorage):
    """
    Drop-in replacement for FileSystemStorage.
    - On save: reads raw bytes → encrypts → writes encrypted blob to disk.
    - On open: reads encrypted blob → decrypts → returns a BytesIO of plaintext.
    """

    def _save(self, name, content):
        """Encrypt file content before writing to disk."""
        raw_data = content.read()
        encrypted = encrypt_data(raw_data)
        return super()._save(name, ContentFile(encrypted))

    def open(self, name, mode='rb'):
        """Read encrypted file from disk and return decrypted content."""
        stored_file = super().open(name, mode)
        encrypted_data = stored_file.read()
        stored_file.close()

        try:
            decrypted = decrypt_data(encrypted_data)
        except (ValueError, Exception):
            # If decryption fails (legacy unencrypted file), return as-is
            return io.BytesIO(encrypted_data)

        return io.BytesIO(decrypted)
