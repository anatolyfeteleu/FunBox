from typing import TYPE_CHECKING

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from extension.serializers import DomainSerializer, StatusSerializer
from extension.views import SerializerClassMapperViewSetMixin
from .clients import Visit as VisitClient
from .serializers import VisitCreateSerialiser, VisitListSerializer


if not TYPE_CHECKING:
    from rest_framework.request import Request


class VisitViewSet(SerializerClassMapperViewSetMixin, GenericAPIView):
    """ViewSet for `visits`"""

    visit_client = VisitClient()

    serializer_class_mapper = {
        'visited_links': VisitCreateSerialiser,
        'visited_domains': VisitListSerializer
    }

    @swagger_auto_schema(responses={status.HTTP_201_CREATED: StatusSerializer()})
    @action(methods=['POST'], detail=False, url_path='visited-links')
    def visited_links(self, request: Request, *args: list, **kwargs: dict):
        """
        Request that registers visited resources at this point in time.

        ### Sample request:
        Request body:
        - links (`<List[str]>`) - array of resource addresses

        Sample body:
        ```
        {
            "links": [
                "https://www.google.com",
                "https://msn.com",
                "https://ya.ru"
            ]
        }
        ```

        Response status codes:
        - 201 - Created
        - 400 - Validation error

        Response body:
        ```
        {
          "status": "ok"
        }
        ```

        Possible `status`:
        - "ok" - successfull request
        - "not ok" - unsuccessfull request
        """

        data = dict()

        _detail = 'ok'
        _status = status.HTTP_201_CREATED

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            _detail = 'not ok'
            _status = status.HTTP_400_BAD_REQUEST
        else:
            self.visit_client.register(serializer.validated_data['links'])

        data.update({'status': _detail})
        return Response(data=data, status=_status)

    @swagger_auto_schema(responses={status.HTTP_200_OK: DomainSerializer()})
    @action(methods=['GET'], detail=False, url_path='visited-domains',)
    def visited_domains(self, request, *args, **kwargs):
        """
        Request that returns visited resources by `from` and `to` parameters in query parameters.

        ### Sample request:

        Request
        `GET: {host}/api/visited-domains?from=123456789&to=123456789`

        Query parameters:
        - from (`<str|int|float>`) - `POSIX` datetime format
        - to (`<str|int|float>`) - `POSIX` datetime format

        Response status codes:
        - 200 - Created

        Response body:
        ```
        {
          "status": "ok",
          "domains": [
              "https://www.google.com",
              "https://msn.com",
              "https://ya.ru"
         ]
        }
        ```

        Possible `status`:
        - "ok" - successfull request
        """

        data = dict(status="ok", domains=list())

        _detail = 'ok'
        _status = status.HTTP_200_OK

        start, end = request.query_params.get('from'), request.query_params.get('to')
        if not start or not end:
            _status = status.HTTP_400_BAD_REQUEST
            _detail = 'not ok'
        else:
            data.update({'domains': self.visit_client.find(start=start, end=end)})

        data.update({'status': _detail})
        return Response(data=data, status=_status)
