from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)

class PostLimitOffsetPagination(LimitOffsetPagination):
    max_limit = 10
    default_limit = 2

class PostPageNumberPagination(LimitOffsetPagination):
    page_size = 2