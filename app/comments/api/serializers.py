from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError
)
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from comments.models import Comment
from users.api.serializers import UserDetailSerializer

User = get_user_model()

def create_comment_serializer(model_type='post', slug=None, parent_id=None, user=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                'id',
                'content',
                'timestamp'
            ]

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None

            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()

            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError('This is not a valid content type')
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=self.slug)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError('This is not a slug for this content type')
            return data

        def create(self, validate_data):
            content = validate_data.get('content')
            if user:
                main_user = user
            else:
                main_user = User.objects.all().first()

            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(model_type, slug, content, main_user, parent_obj)

            return comment

    return CommentCreateSerializer

class CommentListSerializer(ModelSerializer):
    reply_count = SerializerMethodField()
    url = HyperlinkedIdentityField(
        view_name='comments-api:detail'
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'object_id',
            'content_type',
            'parent',
            'content',
            'reply_count',
            'timestamp',
            'user',
            'url'
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

class CommentChildSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'timestamp',
            'user'
        ]

class CommentDetailSerializer(ModelSerializer):
    replies = SerializerMethodField()
    reply_count = SerializerMethodField()
    content_object_url = SerializerMethodField()
    user = UserDetailSerializer(read_only=True)
    edit_url = HyperlinkedIdentityField(
        view_name='comments-api:edit'
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            #'object_id',
            #'content_type',
            'parent',
            'content',
            'replies',
            'reply_count',
            'timestamp',
            'user',
            'edit_url',
            'content_object_url'
        ]

    def get_content_object_url(self, obj):
        try:
            return obj.content_object.get_api_url()
        except:
            return None

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

class CommentEditSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'timestamp'
        ]