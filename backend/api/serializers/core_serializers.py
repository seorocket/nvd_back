from rest_framework import serializers

from core.models import (News, 
                         Announcement,
                         Event,
                         MapPoint,
                         Tag,
                         Post,
                         Topic,
                         NewsCategory)
from ..serializers.user_serializers import UserSerializer


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class MapPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapPoint
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    topic_title = serializers.CharField(source='topic.title', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author', 'topic_title']

class TopicSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    post_count = serializers.IntegerField(source='posts.count', read_only=True)

    class Meta:
        model = Topic
        fields = '__all__'
        read_only_fields = ['author']