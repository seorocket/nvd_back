from rest_framework import serializers
from core.models import NewsletterSubscription


class NewsletterSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate_email(self, value):
        if NewsletterSubscription.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError("Этот email уже подписан на новости.")
        return value