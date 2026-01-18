"""
Tests for Encryption Manager (TDD approach).
"""

import pytest
import hashlib
from datetime import datetime


class TestEncryptionManager:
    """Test cases for EncryptionManager class."""

    def test_init(self, test_config):
        """Test encryption manager initialization."""
        from pseudocode.utils.encryption_manager import EncryptionManager

        manager = EncryptionManager(secret_key=test_config["encryption"]["secret_key"])

        assert manager.secret_key == test_config["encryption"]["secret_key"]
        assert manager.cipher is not None

    def test_encrypt_decrypt(self, test_config):
        """Test encryption and decryption roundtrip."""
        from pseudocode.utils.encryption_manager import EncryptionManager

        manager = EncryptionManager(secret_key=test_config["encryption"]["secret_key"])

        original_data = "sensitive_user_data_123"
        encrypted = manager.encrypt(original_data)
        decrypted = manager.decrypt(encrypted)

        assert encrypted != original_data
        assert decrypted == original_data

    def test_encrypt_same_data_different_output(self, test_config):
        """Test that encrypting same data twice produces different outputs (IV)."""
        from pseudocode.utils.encryption_manager import EncryptionManager

        manager = EncryptionManager(secret_key=test_config["encryption"]["secret_key"])

        data = "test_data"
        encrypted1 = manager.encrypt(data)
        encrypted2 = manager.encrypt(data)

        # With random IV, same data should produce different ciphertext
        assert encrypted1 != encrypted2

    def test_decrypt_invalid_data(self, test_config):
        """Test decrypting invalid data."""
        from pseudocode.utils.encryption_manager import EncryptionManager

        manager = EncryptionManager(secret_key=test_config["encryption"]["secret_key"])

        with pytest.raises(Exception):
            manager.decrypt("invalid_encrypted_data")

    def test_mask_phone(self, test_config):
        """Test phone number masking."""
        from pseudocode.utils.encryption_manager import EncryptionManager

        manager = EncryptionManager(secret_key=test_config["encryption"]["secret_key"])

        phone = "13800138000"
        masked = manager.mask_phone(phone)

        assert masked == "138****8000"

    def test_mask_email(self, test_config):
        """Test email masking."""
        from pseudocode.utils.encryption_manager import EncryptionManager

        manager = EncryptionManager(secret_key=test_config["encryption"]["secret_key"])

        email = "testuser@example.com"
        masked = manager.mask_email(email)

        assert masked == "t***@example.com"

    def test_mask_id_card(self, test_config):
        """Test ID card masking."""
        from pseudocode.utils.encryption_manager import EncryptionManager

        manager = EncryptionManager(secret_key=test_config["encryption"]["secret_key"])

        id_card = "110101199001011234"
        masked = manager.mask_id_card(id_card)

        assert masked == "110101********1234"

    def test_mask_name_chinese(self, test_config):
        """Test Chinese name masking."""
        from pseudocode.utils.encryption_manager import EncryptionManager

        manager = EncryptionManager(secret_key=test_config["encryption"]["secret_key"])

        name = "张三丰"
        masked = manager.mask_name(name)

        assert masked == "张**"

    def test_mask_name_short(self, test_config):
        """Test short name masking."""
        from pseudocode.utils.encryption_manager import EncryptionManager

        manager = EncryptionManager(secret_key=test_config["encryption"]["secret_key"])

        name = "李四"
        masked = manager.mask_name(name)

        # Short names: show first char + **
        assert len(masked) >= 2
        assert masked[0] == "李"

    def test_hash_password(self, test_config):
        """Test password hashing."""
        from pseudocode.utils.encryption_manager import EncryptionManager

        manager = EncryptionManager(secret_key=test_config["encryption"]["secret_key"])

        password = "test_password_123"
        hashed = manager.hash_password(password)

        assert hashed is not None
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        assert hashed != password

    def test_hash_password_same_input_different_hash(self, test_config):
        """Test that same password produces different hash each time (salt)."""
        from pseudocode.utils.encryption_manager import EncryptionManager

        manager = EncryptionManager(secret_key=test_config["encryption"]["secret_key"])

        password = "test_password"
        hash1 = manager.hash_password(password)
        hash2 = manager.hash_password(password)

        # With salt, same password should produce different hashes
        assert hash1 != hash2

    def test_verify_password_valid(self, test_config):
        """Test verifying correct password."""
        from pseudocode.utils.encryption_manager import EncryptionManager

        manager = EncryptionManager(secret_key=test_config["encryption"]["secret_key"])

        password = "correct_password"
        hashed = manager.hash_password(password)

        result = manager.verify_password(password, hashed)

        assert result is True

    def test_verify_password_invalid(self, test_config):
        """Test verifying incorrect password."""
        from pseudocode.utils.encryption_manager import EncryptionManager

        manager = EncryptionManager(secret_key=test_config["encryption"]["secret_key"])

        password = "correct_password"
        hashed = manager.hash_password(password)

        result = manager.verify_password("wrong_password", hashed)

        assert result is False


class TestPasswordHasher:
    """Test cases for PasswordHasher class."""

    def test_hash_password(self):
        """Test password hashing."""
        from pseudocode.utils.encryption_manager import PasswordHasher

        password = "test_password_123"
        hashed = PasswordHasher.hash_password(password)

        assert hashed is not None
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        assert hashed != password

    def test_verify_password_correct(self):
        """Test verifying correct password."""
        from pseudocode.utils.encryption_manager import PasswordHasher

        password = "correct_password"
        hashed = PasswordHasher.hash_password(password)

        result = PasswordHasher.verify_password(password, hashed)

        assert result is True

    def test_verify_password_incorrect(self):
        """Test verifying incorrect password."""
        from pseudocode.utils.encryption_manager import PasswordHasher

        password = "correct_password"
        hashed = PasswordHasher.hash_password(password)

        result = PasswordHasher.verify_password("wrong_password", hashed)

        assert result is False


class TestDataMasker:
    """Test cases for DataMasker class."""

    def test_mask_phone(self):
        """Test phone number masking."""
        from pseudocode.utils.encryption_manager import DataMasker

        assert DataMasker.mask_phone("13800138000") == "138****8000"
        assert DataMasker.mask_phone("15912345678") == "159****5678"

    def test_mask_email(self):
        """Test email masking."""
        from pseudocode.utils.encryption_manager import DataMasker

        assert DataMasker.mask_email("test@example.com") == "t***@example.com"
        assert DataMasker.mask_email("user123@gmail.com") == "u***@gmail.com"

    def test_mask_id_card(self):
        """Test ID card masking."""
        from pseudocode.utils.encryption_manager import DataMasker

        assert DataMasker.mask_id_card("110101199001011234") == "110101********1234"
        assert DataMasker.mask_id_card("440304199502281234") == "440304********1234"

    def test_mask_name_chinese(self):
        """Test Chinese name masking."""
        from pseudocode.utils.encryption_manager import DataMasker

        assert DataMasker.mask_name("张三丰") == "张**"
        assert DataMasker.mask_name("李四") == "李*"
        assert DataMasker.mask_name("王五") == "王*"
