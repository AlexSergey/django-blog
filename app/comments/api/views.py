from django.db.models import Q
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin

from posts.api.pagination import (
    PostLimitOffsetPagination,
    PostPageNumberPagination
)

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)

from comments.models import Comment

from .serializers import (
    CommentDetailSerializer,
    CommentListSerializer,
    create_comment_serializer,
    CommentEditSerializer
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)

from posts.api.permissions import IsOwnerOrReadOnly

class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name']
    pagination_class = PostPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comment.objects.filter(id__gte=0)
        query = self.request.GET.get('q')

        if query:
            queryset_list = queryset_list.filter(
                # if we want to search about title AND content AND user
                Q(title__icontains=query) |
                Q(content__icontains=query)
            ).distinct()

        return queryset_list


class CommentDetailAPIView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer

class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    # serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type = self.request.GET.get('type')
        slug = self.request.GET.get('slug')
        parent_id = self.request.GET.get('parent_id', None)
        user = self.request.user
        return create_comment_serializer(model_type, slug, parent_id, user)

    #def perform_create(self, serializer):
    #    serializer.save(user=self.request.user)

class CommentEditAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentEditSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)