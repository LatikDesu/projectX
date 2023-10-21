from drf_spectacular.openapi import OpenApiResponse
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.views import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import Equipment
from ..serializers import EquipmentSerializer


class EquipmentViewSet(ReadOnlyModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    common_equipment_status_codes = {
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
        summary='Получение списка всех объектов класса "Оборудование"',
        tags=['Equipment'],
        description="""
        Получение списка всех типов оборудования.
        В ответе будет получен список объектов класса "Оборудование".
        """,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=EquipmentSerializer(many=True),
                description='Ответ получен',
                examples=[
                    OpenApiExample(
                        name='Оборудование',
                        value={
                            "id": 1,
                            "name": "software",
                            "description": "Собирает и обрабатывает информацию о растениях и почве"
                        }

                    )
                ]
            ),
            **common_equipment_status_codes
        }
    )
    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        exclude=True,
        summary='Получение конкретного объекта класса "Оборудование"',
        tags=['Equipment'],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=EquipmentSerializer,
                description='OK'
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=None,
                description='Объект не найден'
            ),
            **common_equipment_status_codes
        }
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Equipment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @extend_schema(
    #     summary='Создание объекта класса "Оборудование"',
    #     tags=['Equipment'],
    #     request=EquipmentSerializer,
    #     responses={
    #         status.HTTP_201_CREATED: OpenApiResponse(
    #             response=EquipmentSerializer,
    #             description='Создано'
    #         ),
    #         **common_equipment_status_codes
    #     },
    #     examples=[
    #         OpenApiExample(
    #             name='Пример',
    #             value={
    #                 "name": "BFG9000",
    #                 "description": "Big Fucking Gun",
    #                 "price": 666,
    #                 "availability": True,
    #                 "equipment_shop_id": 1,
    #             }
    #         )
    #     ]
    # )
    # def create(self, request, *args, **kwargs):
    #     try:
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_create(serializer)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #
    # @extend_schema(
    #     summary='Обновление информации об объекте класса "Оборудование"',
    #     tags=['Equipment'],
    #     request=EquipmentSerializer,
    #     responses={
    #         status.HTTP_200_OK: OpenApiResponse(
    #             response=EquipmentSerializer,
    #             description='Создано'
    #         ),
    #         status.HTTP_404_NOT_FOUND: OpenApiResponse(
    #             response=None,
    #             description='Объект не найден'
    #         ),
    #         **common_equipment_status_codes
    #     }
    # )
    # def update(self, request, *args, **kwargs):
    #     try:
    #         partial = kwargs.pop('partial', False)
    #         instance = self.get_object()
    #         serializer = self.get_serializer(
    #             instance, data=request.data, partial=partial)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_update(serializer)
    #         if getattr(instance, '_prefetched_objects_cache', None):
    #             instance._prefetched_objects_cache = {}
    #         return Response(serializer.data)
    #     except Equipment.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #
    # @extend_schema(
    #     summary='Добавление информации к объекту класса "Оборудование"',
    #     tags=['Equipment'],
    #     request=EquipmentSerializer,
    #     responses={
    #         status.HTTP_200_OK: OpenApiResponse(
    #             response=EquipmentSerializer,
    #             description='Создано'
    #         ),
    #         status.HTTP_404_NOT_FOUND: OpenApiResponse(
    #             response=None,
    #             description='Объект не найден'
    #         ),
    #         **common_equipment_status_codes
    #     }
    # )
    # def partial_update(self, request, *args, **kwargs):
    #     try:
    #         kwargs['partial'] = True
    #         return self.update(request, *args, **kwargs)
    #     except Equipment.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #
    # @extend_schema(
    #     summary='Удаление объекта класса "Оборудование"',
    #     tags=['Equipment'],
    #     responses={
    #         status.HTTP_204_NO_CONTENT: OpenApiResponse(
    #             response=None,
    #             description='OK'
    #         ),
    #         status.HTTP_404_NOT_FOUND: OpenApiResponse(
    #             response=None,
    #             description='Объект не найден'
    #         ),
    #         **common_equipment_status_codes
    #     }
    # )
    # def destroy(self, request, *args, **kwargs):
    #     try:
    #         instance = self.get_object()
    #         self.perform_destroy(instance)
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     except Equipment.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
