from django.db import models


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Подписка на новости"
        verbose_name_plural = "Подписки на новости"
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email