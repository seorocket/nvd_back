from rest_framework import serializers, validators
from django.contrib.auth import get_user_model


User = get_user_model()

class TelegramAuthSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    auth_date = serializers.IntegerField()
    hash = serializers.CharField()
    
    def validate(self, attrs):
        data_hash = attrs['hash']
        del attrs['hash']
        
        # Проверяем валидность данных Telegram
        if not self.verify_telegram_data(attrs, data_hash):
            raise serializers.ValidationError('Invalid Telegram data')
        
        return attrs
    
    def verify_telegram_data(self, data, received_hash):
        """
        Проверяет валидность данных от Telegram Web App
        """
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not bot_token:
            raise serializers.ValidationError('Telegram bot token not configured')
        
        # Создаем строку для проверки
        data_check_string = '\n'.join([f'{k}={v}' for k, v in sorted(data.items())])
        
        # Вычисляем секретный ключ
        secret_key = hashlib.sha256(bot_token.encode()).digest()
        
        # Вычисляем хеш
        computed_hash = hmac.new(
            secret_key, 
            data_check_string.encode(), 
            hashlib.sha256
        ).hexdigest()
        
        return computed_hash == received_hash
    
    def create(self, validated_data):
        telegram_id = validated_data['id']
        
        # Ищем существующего пользователя по telegram_id
        try:
            telegram_user = TelegramUser.objects.get(telegram_id=telegram_id)
            return telegram_user.user
        except TelegramUser.DoesNotExist:
            pass
        
        # Создаем нового пользователя
        username = self.generate_username(validated_data)
        user = User.objects.create_user(
            username=username,
            email=f"{telegram_id}@telegram.user",  # Заглушка для email
            password=None
        )
        
        # Создаем запись TelegramUser
        TelegramUser.objects.create(
            user=user,
            telegram_id=telegram_id,
            username=validated_data.get('username'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            auth_date=validated_data['auth_date']
        )
        
        return user
    
    def generate_username(self, data):
        """Генерирует уникальное имя пользователя"""
        base_username = data.get('username') or f"tg_{data['id']}"
        username = base_username
        counter = 1
        
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1
            
        return username