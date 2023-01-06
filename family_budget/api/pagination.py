from rest_framework.pagination import (  
    LimitOffsetPagination,
    PageNumberPagination,
)


class ProjectLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 2


class ProjectPageNumberPagination(PageNumberPagination):
    page_size = 3