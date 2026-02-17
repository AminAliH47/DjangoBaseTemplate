from rest_framework.response import Response
from rest_framework import serializers, views, pagination
from django.db.models import QuerySet


def get_paginated_response(
    *,
    pagination_class: pagination.BasePagination,
    serializer_class: serializers.Serializer,
    queryset: QuerySet,
    request,
    view: views.APIView,
):
    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(
            page,
            many=True,
            context={'request': request}
        )
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)

    return Response(data=serializer.data)
