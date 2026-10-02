# tests/test_crypto_utils.py
import pytest
from src.utils import (
    encrypt_email,
    decrypt_email,
    hash_password,
    verify_password,
    get_encryption_salt
)

def test_encryption_salt():
    salt = get_encryption_salt()
    assert isinstance(salt, str)
    assert len(salt) > 0

def test_email_encryption_and_decryption():
    email = "desenvolvedor@python.org"
    encrypted = encrypt_email(email)
    assert encrypted != email
    assert isinstance(encrypted, str)
    assert len(encrypted) > 0

    decrypted = decrypt_email(encrypted)
    assert decrypted == email

def test_email_decryption_empty_or_invalid():
    assert decrypt_email("") == ""
    assert decrypt_email("invalid_base64_payload!!!") == ""

def test_password_hashing_and_verification():
    password = "minha_senha_super_segura_123"
    pwd_hash, salt = hash_password(password)

    assert pwd_hash is not None
    assert salt is not None
    assert len(pwd_hash) == 64 # SHA-256 hex string

    # Verificação de senha correta
    assert verify_password(password, pwd_hash, salt) is True

    # Verificação de senha incorreta
    assert verify_password("senha_errada", pwd_hash, salt) is False

def test_password_verification_empty():
    assert verify_password("", "hash", "salt") is False
    assert verify_password("pass", "", "salt") is False
    assert verify_password("pass", "hash", "") is False
