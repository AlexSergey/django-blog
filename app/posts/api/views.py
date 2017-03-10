from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
)

from .pagination import (
    PostPageNumberPagination
)

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)

from posts.models import Post
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostCreateUpdateSerializer
)

from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)

from .permissions import IsOwnerOrReadOnly

class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    pagination_class = PostPageNumberPagination

    ## Alternative query search from post list - ?q=<query>
    #def get_queryset(self, *args, **kwargs):
    #    queryset_list = Post.objects.all()
    #    query = self.request.GET.get('q')

    #    if query:
    #        queryset_list = queryset_list.filter(
    #            # if we want to search about title AND content AND user
    #            Q(title__icontains=query) |
    #            Q(content__icontains=query)
    #        ).distinct()

    #   return queryset_list


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)