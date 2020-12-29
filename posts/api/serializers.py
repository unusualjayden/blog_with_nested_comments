from rest_framework.serializers import ModelSerializer

from posts.models import Post, Comment


class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'title',
            'author',
            'slug',
            'body',
            'publish',
        )


class PostDetailSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'title',
            'author',
            'body',
            'publish',
            'status',
        )


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'parent', 'content')
        read_only_fields = ('id', 'author', 'post', 'parent')
