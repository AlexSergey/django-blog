from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)

from posts.models import Post
from users.api.serializers import UserDetailSerializer

post_detail_url = HyperlinkedIdentityField(
    view_name='posts-api:detail',
    lookup_field='slug'
)
post_delete_url = HyperlinkedIdentityField(
    view_name='posts-api:detail',
    lookup_field='slug'
)

from comments.api.serializers import CommentListSerializer
from comments.models import Comment

class PostListSerializer(ModelSerializer):
    url = post_detail_url
    user = UserDetailSerializer(read_only=True)
    class Meta:
        model = Post
        fields = [
            'user',
            'title',
            'content',
            'publish',
            'url'
        ]

    def get_user(self, obj):
        return str(obj.user.username)

class PostDetailSerializer(ModelSerializer):
    url = post_detail_url
    delete_url = post_delete_url
    user = UserDetailSerializer(read_only=True)
    image = SerializerMethodField()
    html = SerializerMethodField()

    comments = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'content',
            'publish',
            'url',
            'delete_url',
            'html',
            'user',
            'image',
            'comments'
        ]

    def get_html(self, obj):
        return obj.get_markdown()

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_user(self, obj):
        return str(obj.user.username)

    def get_comments(self, obj):
        comments_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentListSerializer(comments_qs, many=True).data
        return comments

class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'publish'
        ]