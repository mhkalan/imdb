from rest_framework.pagination import CursorPagination


# class ContentPagination(PageNumberPagination):
#     page_size = 4
#     page_query_param = 'p'


class ContentCursorPagination(CursorPagination):
    page_size = 4
    ordering = 'date'





