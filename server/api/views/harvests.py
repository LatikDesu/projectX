from drf_spectacular.openapi import OpenApiResponse
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.views import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import Harvest
from ..serializers import HarvestSerializer


class HarvestViewSet(ReadOnlyModelViewSet):
    queryset = Harvest.objects.all()
    serializer_class = HarvestSerializer

    common_harvest_status_codes = {
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=None,
            description='Неправильный запрос'
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            response=None,
            description='Пользователь не авторизован'
        ),
        status.HTTP_403_FORBIDDEN: OpenApiResponse(
            response=None,
            description='Доступ запрещён'
        ),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(
            response=None,
            description='Запрашиваемый объект не найден'
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
            response=None,
            description='Внутренняя ошибка сервера'
        )
    }

    @extend_schema(
        summary='Получение списка всех объектов класса "Урожай"',
        tags=['Harvest'],
        description="""
        Получение списка всех типов урожая.
        В ответе будет получен список объектов класса "Урожай".
        """,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=HarvestSerializer(many=True),
                description='Ответ получен',
                examples=[
                    OpenApiExample(
                        name='Урожай',
                        value={
                            "id": 1,
                            "name": "tomatoes",
                            "description": "Помидоры"
                        }
                    )
                ]
            ),
            **common_harvest_status_codes
        }
    )
    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        exclude=True,
        summary='Получение конкретного объекта класса "Урожай"',
        tags=['Harvest'],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=HarvestSerializer,
                description='OK'
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=None,
                description='Объект не найден'
            ),
            **common_harvest_status_codes
        }
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Harvest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @extend_schema(
    #     summary='Создание объекта класса "Урожай"',
    #     tags=['Harvest'],
    #     request=HarvestSerializer,
    #     responses={
    #         status.HTTP_201_CREATED: OpenApiResponse(
    #             response=HarvestSerializer,
    #             description='Создано'
    #         ),
    #         status.HTTP_400_BAD_REQUEST: OpenApiResponse(
    #             response=None,
    #             description='Неправильный запрос'
    #         ),
    #         status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
    #             response=None,
    #             description='Пользователь не авторизован'
    #         ),
    #         status.HTTP_403_FORBIDDEN: OpenApiResponse(
    #             response=None,
    #             description='Доступ запрещён'
    #         ),
    #         status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
    #             response=None,
    #             description='Внутренняя ошибка сервера'
    #         )
    #     },
    #     examples=[
    #         OpenApiExample(
    #             name='Пример',
    #             value={
    #                 "name": "Pineapple",
    #                 "description": "description of pineapple",
    #                 "price": 200,
    #                 "availability": True,
    #                 "gen_modified": False,
    #                 "harvest_shop_id": 1,
    #             }
    #         )
    #     ]
    # )
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # @extend_schema(
    #     summary='Обновление информации об объекте класса "Урожай"',
    #     tags=['Harvest'],
    #     responses=harvest_status_codes)
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(
    #         instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}

    #     return Response(serializer.data)

    # @extend_schema(
    #     summary='Добавление информации к объекту класса "Урожай"',
    #     tags=['Harvest'],
    #     responses=harvest_status_codes,
    # )
    # def partial_update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return self.update(request, *args, **kwargs)

    # @extend_schema(
    #     summary='Удаление объекта класса "Урожай"',
    #     tags=['Harvest'],
    #     responses={
    #         status.HTTP_200_OK: OpenApiResponse(
    #             response=None,
    #             description='OK'
    #         ),
    #         status.HTTP_400_BAD_REQUEST: OpenApiResponse(
    #             response=None,
    #             description='Неправильный запрос'
    #         ),
    #         status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
    #             response=None,
    #             description='Пользователь не авторизован'
    #         ),
    #         status.HTTP_403_FORBIDDEN: OpenApiResponse(
    #             response=None,
    #             description='Доступ запрещён'
    #         ),
    #         status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
    #             response=None,
    #             description='Внутренняя ошибка сервера'
    #         )
    #     }
    # )
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
