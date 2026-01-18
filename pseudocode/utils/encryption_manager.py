# 加密管理器实现代码
# 文件路径: utils/encryption_manager.py

from typing import Optional, Dict
from cryptography.fernet import Fernet
import base64
import hashlib
import bcrypt


class EncryptionManager:
    """加密管理器"""

    def __init__(self, secret_key: str):
        """
        初始化加密管理器

        Args:
            secret_key: 密钥
        """
        key = hashlib.sha256(secret_key.encode()).digest()
        self.cipher = Fernet(base64.urlsafe_b64encode(key))

    def encrypt(self, data: str) -> str:
        """
        加密数据

        Args:
            data: 明文数据

        Returns:
            密文数据（Base64编码）
        """
        encrypted = self.cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """
        解密数据

        Args:
            encrypted_data: 密文数据（Base64编码）

        Returns:
            明文数据
        """
        try:
            encrypted = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self.cipher.decrypt(encrypted)
            return decrypted.decode()
        except Exception:
            raise Exception("Invalid encrypted data")

    def encrypt_sensitive_data(self, data: str, data_type: str) -> str:
        """
        加密敏感数据（通用方法）

        Args:
            data: 敏感数据
            data_type: 数据类型（phone/email/id_card/general）

        Returns:
            加密后的数据
        """
        if data_type == "phone":
            return self.encrypt_phone(data)
        elif data_type == "email":
            return self.encrypt_email(data)
        elif data_type == "id_card":
            return self.encrypt_id_card(data)
        else:
            return self.encrypt(data)

    def encrypt_phone(self, phone: str) -> str:
        """
        加密手机号

        Args:
            phone: 手机号

        Returns:
            加密后的手机号
        """
        masked = DataMasker.mask_phone(phone)
        return self.encrypt(masked)

    def encrypt_email(self, email: str) -> str:
        """
        加密邮箱

        Args:
            email: 邮箱

        Returns:
            加密后的邮箱
        """
        masked = DataMasker.mask_email(email)
        return self.encrypt(masked)

    def encrypt_id_card(self, id_card: str) -> str:
        """
        加密身份证号

        Args:
            id_card: 身份证号

        Returns:
            加密后的身份证号
        """
        masked = DataMasker.mask_id_card(id_card)
        return self.encrypt(masked)

    def mask_phone(self, phone: str) -> str:
        """手机号脱敏"""
        return DataMasker.mask_phone(phone)

    def mask_email(self, email: str) -> str:
        """邮箱脱敏"""
        return DataMasker.mask_email(email)

    def mask_id_card(self, id_card: str) -> str:
        """身份证号脱敏"""
        return DataMasker.mask_id_card(id_card)

    def mask_name(self, name: str) -> str:
        """姓名脱敏"""
        return DataMasker.mask_name(name)

    def hash_password(self, password: str) -> str:
        """
        哈希密码

        Args:
            password: 明文密码

        Returns:
            哈希后的密码
        """
        return PasswordHasher.hash_password(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        验证密码

        Args:
            password: 明文密码
            hashed_password: 哈希密码

        Returns:
            是否匹配
        """
        return PasswordHasher.verify_password(password, hashed_password)


class PasswordHasher:
    """密码哈希器"""

    SALT_ROUNDS = 12

    @staticmethod
    def hash_password(password: str) -> str:
        """
        哈希密码

        Args:
            password: 明文密码

        Returns:
            哈希后的密码
        """
        salt = bcrypt.gensalt(rounds=PasswordHasher.SALT_ROUNDS)
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        验证密码

        Args:
            password: 明文密码
            hashed_password: 哈希密码

        Returns:
            是否匹配
        """
        try:
            return bcrypt.checkpw(password.encode(), hashed_password.encode())
        except (ValueError, TypeError):
            return False


class DataMasker:
    """数据脱敏器"""

    @staticmethod
    def mask_phone(phone: str, mask_char: str = "*") -> str:
        """
        脱敏手机号

        Args:
            phone: 手机号
            mask_char: 掩码字符

        Returns:
            脱敏后的手机号
        """
        if len(phone) < 7:
            return phone
        return phone[:3] + mask_char * 4 + phone[-4:]

    @staticmethod
    def mask_email(email: str, mask_char: str = "*") -> str:
        """
        脱敏邮箱

        Args:
            email: 邮箱
            mask_char: 掩码字符

        Returns:
            脱敏后的邮箱
        """
        parts = email.split("@")
        if len(parts) != 2:
            return email

        username = parts[0]
        if len(username) <= 1:
            masked_username = username
        else:
            masked_username = username[0] + mask_char * (len(username) - 1)

        return f"{masked_username}@{parts[1]}"

    @staticmethod
    def mask_id_card(id_card: str, mask_char: str = "*") -> str:
        """
        脱敏身份证号

        Args:
            id_card: 身份证号
            mask_char: 掩码字符

        Returns:
            脱敏后的身份证号
        """
        if len(id_card) < 10:
            return id_card
        return id_card[:6] + mask_char * 8 + id_card[-4:]

    @staticmethod
    def mask_name(name: str, mask_char: str = "*") -> str:
        """
        脱敏姓名

        Args:
            name: 姓名
            mask_char: 掩码字符

        Returns:
            脱敏后的姓名
        """
        if len(name) <= 1:
            return name
        return name[0] + mask_char * (len(name) - 1)

    @staticmethod
    def mask_address(address: str, mask_char: str = "*", keep_chars: int = 6) -> str:
        """
        脱敏地址

        Args:
            address: 地址
            mask_char: 掩码字符
            keep_chars: 保留字符数

        Returns:
            脱敏后的地址
        """
        if len(address) <= keep_chars:
            return address
        return address[:keep_chars] + mask_char * (len(address) - keep_chars)


class EncryptionConfig:
    """加密配置"""

    SENSITIVE_DATA_TYPES = [
        "phone",
        "email",
        "id_card",
        "bank_card",
        "password",
        "general",
    ]

    MASKING_RULES = {
        "phone": {"keep_prefix": 3, "keep_suffix": 4},
        "email": {"keep_prefix": 1, "keep_suffix": 0},
        "id_card": {"keep_prefix": 6, "keep_suffix": 4},
        "bank_card": {"keep_prefix": 6, "keep_suffix": 4},
        "name": {"keep_prefix": 1, "keep_suffix": 0},
    }

    @classmethod
    def get_masking_rule(cls, data_type: str) -> Dict[str, int]:
        """
        获取脱敏规则

        Args:
            data_type: 数据类型

        Returns:
            脱敏规则
        """
        return cls.MASKING_RULES.get(data_type, {"keep_prefix": 0, "keep_suffix": 0})

    @classmethod
    def is_sensitive_data(cls, data_type: str) -> bool:
        """
        检查是否为敏感数据

        Args:
            data_type: 数据类型

        Returns:
            是否为敏感数据
        """
        return data_type in cls.SENSITIVE_DATA_TYPES
