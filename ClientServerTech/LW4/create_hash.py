from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Генерируем хэш для пароля "test"
password = "test"
hash_value = pwd_context.hash(password)

print(f"Пароль: {password}")
print(f"Хэш: {hash_value}")
print("\nСкопируйте этот хэш в users_db:")
print(f'"password": "{hash_value}"')