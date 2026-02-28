import secrets
import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

print("\n--- GENERATING KEYS ---")

# 1. Generate AES 256 Key (Secret Key)
aes_key = base64.b64encode(secrets.token_bytes(32)).decode()
print(f"SECRET_KEY_B64=\"{aes_key}\"\n")

# 2. Generate RSA Key Pair (JWT Keys)
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
).decode()

public_key = private_key.public_key()
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode()

print("JWT_PRIVATE_KEY=\"\"\"" + private_pem + "\"\"\"")
print("\nJWT_PUBLIC_KEY=\"\"\"" + public_pem + "\"\"\"")
print("--- GENERATION COMPLETE ---")