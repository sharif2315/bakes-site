from urllib.parse import urlencode
from django.http import HttpRequest


def build_pagination_query(request: HttpRequest):
    query_params = request.GET.copy()
    query_params.pop("page", None)  # Remove existing 'page' if any
    return urlencode(query_params) 