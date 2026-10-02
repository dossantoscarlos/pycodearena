# src/utils/crypto_utils.py
import os
import hashlib
import hmac
import secrets
import base64

def load_dotenv():
    """
    Carrega as variáveis de ambiente do arquivo .env sem depender de bibliotecas externas.
    """
    # Raiz do projeto (3 níveis acima de src/utils/crypto_utils.py)
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    env_path = os.path.join(root_dir, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key not in os.environ:
                        os.environ[key] = val

# Carrega as variáveis do .env imediatamente na importação
load_dotenv()

def get_encryption_salt() -> str:
    """
    Obtém a salt de criptografia do arquivo .env.
    """
    salt = os.getenv("ENCRYPTION_SALT")
    if not salt:
        salt = "PyCodeArena_Default_Secure_Salt_2026"
    return salt

def encrypt_email(email: str) -> str:
    """
    Criptografa o e-mail de recuperação usando PBKDF2 + Stream Cipher XOR + HMAC SHA-256
    fundamentado no ENCRYPTION_SALT do .env.
    """
    if not email:
        return ""
    
    salt_key = get_encryption_salt().encode('utf-8')
    plain_bytes = email.strip().encode('utf-8')
    
    # Gerador de IV aleatório de 16 bytes
    iv = secrets.token_bytes(16)
    
    # Derivação de chave usando PBKDF2 HMAC SHA-256
    key_stream = hashlib.pbkdf2_hmac('sha256', salt_key, iv, 50000, dklen=len(plain_bytes) + 32)
    cipher_key = key_stream[:len(plain_bytes)]
    mac_key = key_stream[len(plain_bytes):]
    
    # Criptografia XOR por fluxo de bytes
    cipher_bytes = bytes(p ^ k for p, k in zip(plain_bytes, cipher_key))
    
    # Assinatura HMAC para integridade
    tag = hmac.new(mac_key, iv + cipher_bytes, hashlib.sha256).digest()
    
    # Retorna em formato Base64 url-safe
    payload = iv + tag + cipher_bytes
    return base64.urlsafe_b64encode(payload).decode('utf-8')

def decrypt_email(encrypted_str: str) -> str:
    """
    Descriptografa o e-mail usando a salt do .env.
    """
    if not encrypted_str:
        return ""
    
    try:
        salt_key = get_encryption_salt().encode('utf-8')
        raw_payload = base64.urlsafe_b64decode(encrypted_str.encode('utf-8'))
        
        if len(raw_payload) < 48: # 16 (IV) + 32 (MAC)
            return ""
        
        iv = raw_payload[:16]
        tag = raw_payload[16:48]
        cipher_bytes = raw_payload[48:]
        
        key_stream = hashlib.pbkdf2_hmac('sha256', salt_key, iv, 50000, dklen=len(cipher_bytes) + 32)
        cipher_key = key_stream[:len(cipher_bytes)]
        mac_key = key_stream[len(cipher_bytes):]
        
        # Verifica integridade HMAC
        computed_tag = hmac.new(mac_key, iv + cipher_bytes, hashlib.sha256).digest()
        if not hmac.compare_digest(tag, computed_tag):
            print("Alerta: Falha de verificação HMAC na descriptografia do e-mail.")
            return ""
        
        plain_bytes = bytes(c ^ k for c, k in zip(cipher_bytes, cipher_key))
        return plain_bytes.decode('utf-8')
    except Exception as e:
        print(f"Erro ao descriptografar e-mail: {e}")
        return ""

def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """
    Gera um hash PBKDF2 HMAC SHA-256 seguro para a senha.
    Retorna tupla: (password_hash_hex, salt)
    """
    if not salt:
        salt = secrets.token_hex(16)
    
    pwd_bytes = password.encode('utf-8')
    salt_bytes = salt.encode('utf-8')
    
    hash_bytes = hashlib.pbkdf2_hmac('sha256', pwd_bytes, salt_bytes, 100000)
    return hash_bytes.hex(), salt

def verify_password(password: str, stored_hash: str, stored_salt: str) -> bool:
    """
    Valida a senha digitada contra o hash e salt armazenados no banco.
    """
    if not password or not stored_hash or not stored_salt:
        return False
    
    computed_hash, _ = hash_password(password, stored_salt)
    return hmac.compare_digest(computed_hash, stored_hash)
