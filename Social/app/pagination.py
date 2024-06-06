from rest_framework.pagination import LimitOffsetPagination

class myPagination(LimitOffsetPagination):
    default_limit=4
    limit_query_param='limit'
    offset_query_param='offset'
    max_limit=10
