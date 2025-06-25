import os
import jwt
import base64
from config import Config
from typing import Any, Dict, Optional
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Atteribute of child class will be staticmethods by defult
class StaticMethodMeta(type):
    def __new__(cls, name, bases, dct) -> type:
        new_dct = {}
        for key, value in dct.items():
            if callable(value) and not key.startswith('__'):
                value = staticmethod(value)
            new_dct[key] = value
        return super().__new__(cls,name, bases, new_dct)

class SecurityManager():
    def __init__(self):
        self._fernet = Fernet(self._get_or_create_key())
        
    def _get_or_create_key(self) -> bytes:
        """Get existing or create new encryption key"""
        key_file = Config.DATABASE_DIR / ".key"
        if key_file.exists():
            return key_file.read_bytes()
            pass
        Config.init()
        key = Fernet.generate_key()
        key_file.write_bytes(key)
        return key
    
    def encrypt_data(self, data: bytes) -> bytes:
        """Encrypt binary data"""
        return self._fernet.encrypt(data)
    
    def decrypt_data(self, encrypted_data: bytes) -> bytes:
        """Decrypt binary data"""
        return self._fernet.decrypt(encrypted_data)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password for storage"""
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.b64encode(kdf.derive(password.encode()))
        return f"{base64.b64encode(salt).decode()}:{key.decode()}"
    
    @staticmethod
    def verify_password(stored_password: str, provided_password: str) -> bool:
        """Verify a password against its hash"""
        salt, key = stored_password.split(":")
        salt = base64.b64decode(salt.encode())
        stored_key = base64.b64decode(key.encode())
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        try:
            test_key = kdf.derive(provided_password.encode())
            return test_key == stored_key
        except:
            return False
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, Config.SECRET_KEY, algorithm="HS256")
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify a JWT token"""
        try:
            return jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        except jwt.PyJWTError:
            return None
        
if(__name__ == "__main__"):
    print(SecurityManager.verify_password(SecurityManager.hash_password("aavart"),"aavart"))
    pass 
