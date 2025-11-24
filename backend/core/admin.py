from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from core.models import (News, 
                         Announcement,
                         Event,
                         Gallery,
                         Tag,
                         Post,
                         Topic,
                         NewsCategory)



class TagAdmin(admin.ModelAdmin):
    model = Tag
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class NewsAdmin(admin.ModelAdmin):
    search_fields = ("title", "tags", "category", "tags")
    list_filter = ("title", "tags", "category", "tags")
    empty_value_display = "-пусто-"

class AnnouncementAdmin(admin.ModelAdmin):
    search_fields = ("user", "title", "category", "price")
    list_filter = ("user", "title", "category", "price")
    empty_value_display = "-пусто-"


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['image', 'photo_thumbnail']
    search_fields = ['image', 'photo_thumbnail']


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_time', 'location', 'created_at']
    list_filter = ['date_time', 'created_at']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'date_time'



class ForumTopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'author__username']


class ForumPostAdmin(admin.ModelAdmin):
    list_display = ['author', 'topic', 'content', 'created_at', 'parent_post']
    list_filter = ['created_at', 'topic', 'author']
    search_fields = ['content', 'author__username']
    raw_id_fields = ['topic', 'author', 'parent_post']

admin.site.register(Tag, TagAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(NewsCategory, NewsCategoryAdmin)
admin.site.register(Post, ForumPostAdmin)
admin.site.register(Topic,ForumTopicAdmin)