from rest_framework import serializers
from .models import Post
from .services import fetch_github_raw_text


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
    
    def create(self, validated_data):
        validated_data['overview'] = fetch_github_raw_text(validated_data['post_url'])
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.overview = fetch_github_raw_text(validated_data['post_url'])
        instance.post_url = validated_data.get('post_url', instance.post_url)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        instance.save()
        return instance