

import hashlib
import hmac
import urllib.parse
import time

# ВАЖНО: замените на токен вашего бота
BOT_TOKEN = "8382027985:AAFd3cK9TRjHQUrjs1HAP4HlZQpqxffO5dA"

# Данные пользователя для генерации (любые корректные)
user_data = {
    "id": 123456789,  # Уникальный ID пользователя в Telegram
    "first_name": "Test",
    "last_name": "User",
    "username": "testuser",
    "auth_date": str(int(time.time())), # Текущее время
}

# Шаг 1: Сформировать строку данных (data_check_string)
# Сортировка обязательна!
sorted_data = sorted(user_data.items())
data_check_string = "\n".join([f"{k}={v}" for k, v in sorted_data])

print("--- Data Check String (для отладки) ---")
print(data_check_string)
print("---")

# Шаг 2: Создать ключ шифрования (secret key) из токена бота
secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()

# Шаг 3: Вычислить HMAC-SHA-256 хэш от data_check_string
calculated_hash = hmac.new(
    secret_key,
    data_check_string.encode(),
    hashlib.sha256
).hexdigest()

# Шаг 4: Добавить вычисленный hash к user_data
user_data['hash'] = calculated_hash

# Шаг 5: Сформировать initData (URL-кодированная строка)
init_data = urllib.parse.urlencode(user_data)

print("--- Generated initData ---")
print(init_data)
print("---")