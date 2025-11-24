from django.db import models
from users.models import User
from ckeditor.fields import RichTextField

class Topic(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок темы")
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор темы")

    class Meta:
        verbose_name = "Тема форума"
        verbose_name_plural = "Темы форума"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, 
                              related_name='posts', 
                              verbose_name="Тема")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    # content = models.TextField(verbose_name="Содержание")
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_post = models.ForeignKey('self', on_delete=models.SET_NULL, 
                                    null=True, blank=True, 
                                    related_name='replies', 
                                    verbose_name="Родительское сообщение")

    class Meta:
        verbose_name = "Сообщение форума"
        verbose_name_plural = "Сообщения форума"
        ordering = ['created_at']

    def __str__(self):
        return f"Пост от {self.author.username} в теме {self.topic.title}"