import bcrypt

def hash_password(password: str) -> str:
    """Gera hash da senha usando bcrypt."""
    # Codifica a senha para bytes
    password_bytes = password.encode('utf-8')
    # Gera o salt e faz o hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Retorna como string
    return hashed.decode('utf-8')

def get_password_hash(password: str) -> str:
    """Alias para hash_password para compatibilidade."""
    return hash_password(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifica se a senha corresponde ao hash."""
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)