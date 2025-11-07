from django.contrib import admin

from core.models import (News, 
                         Announcement,
                         Event,
                         MapPoint,
                         Tag,
                         Post,
                         Topic,
                         NewsCategory)



class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


class NewsAdmin(admin.ModelAdmin):
    search_fields = ("title", "tags", "category", "tags")
    list_filter = ("title", "tags", "category", "tags")
    empty_value_display = "-пусто-"

admin.site.register(Tag, TagAdmin)
admin.site.register(News, NewsAdmin)