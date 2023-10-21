from drf_spectacular.openapi import OpenApiResponse
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.views import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import Minigame
from ..serializers import MinigameSerializer


class MinigameViewSet(ReadOnlyModelViewSet):
    queryset = Minigame.objects.all()
    serializer_class = MinigameSerializer

    common_minigame_status_codes = {

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
        summary='Получение списка всех доступных Мини-игр',
        tags=['Minigame'],
        description="""
        Получение списка всех мини-игр.
        В ответе будет получен список объектов класса "Миниигра".
        """,
        responses={status.HTTP_200_OK: OpenApiResponse(
            response=MinigameSerializer,
            description='Запрос успешно выполнен',
            examples=[OpenApiExample(
                'Список миниигр',
                value={
                    "id": 1,
                    "name": "gameOne",
                    "description": "Действие игры происходит в небольшой лаборатории, где работает Маша. На столе стоит подставка для пробирок и в ней пробирки с разными геномами растений для скрещивания. Напротив стоит Маша и подсказывает какие надо пробирки брать и смешивать.",
                    "achievement": "\"Мастер скрещивания\": Успешно смешайте все доступные пробирки и создайте все модифицированные растения."
                })]
        ),
            **common_minigame_status_codes
        }
    )
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        exclude=True,
        summary='Получение Миниигры по идентификатору',
        tags=['Minigame'],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=MinigameSerializer,
                description='OK'
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=None,
                description='Объект не найден'
            ),
            **common_minigame_status_codes
        }
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Minigame.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @extend_schema(
    #     summary='Создание объекта класса "Миниигра"',
    #     tags=['Minigame'],
    #     request=MinigameSerializer,
    #     responses={
    #         status.HTTP_201_CREATED: OpenApiResponse(
    #             response=MinigameSerializer,
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
    #                 "name": "Game One",
    #                 "description": "description of game",
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
    #     summary='Обновление информации об объекте класса "Миниигра"',
    #     tags=['Minigame'],
    #     responses=minigame_status_codes)
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(
    #         instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         instance._prefetched_objects_cache = {}

    #     return Response(serializer.data)

    # @extend_schema(
    #     summary='Добавление информации к объекту класса "Миниигра"',
    #     tags=['Minigame'],
    #     responses=minigame_status_codes,
    # )
    # def partial_update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return self.update(request, *args, **kwargs)

    # @extend_schema(
    #     summary='Удаление объекта класса "Миниигра"',
    #     tags=['Minigame'],
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
