from app.core.security import hash_password

password = "password123"

hashed = hash_password(password)

print(hashed)