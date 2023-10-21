from drf_spectacular.utils import OpenApiExample
from drf_spectacular.openapi import OpenApiResponse
from rest_framework import status
from drf_spectacular.views import extend_schema
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from ..models import Player
from ..serializers import PlayerSerializer, LeaderboardPlayerSerializer, PlayerMinigameSerializer


class LiderboardView(ReadOnlyModelViewSet):
    serializer_class = LeaderboardPlayerSerializer

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

    def get_queryset(self):
        queryset = Player.objects.filter(
            top_score__gt=0).order_by('-top_score')[:100]
        return queryset

    @extend_schema(
        summary='Получить 100 лучших игроков по очкам',
        tags=['Liderboard'],
        description="""
            Список 100 лучших игроков по очкам.
            Ранжирование по атрибиту top_score в порядке убывания.
            """,
        request=PlayerSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=LeaderboardPlayerSerializer,
                description='Ответ получен',
                examples=[
                    OpenApiExample(
                        name='Список лидеров',
                        value=[
                            {
                                "name": "Doom Guy",
                                "own_coins": 751,
                                "own_money": 5000,
                                "top_score": 751,
                                "achievement": {
                                    "gameOne": {
                                        "achievement": False
                                    },
                                    "gameTwo": {
                                        "achievement": False
                                    },
                                    "gameThree": {
                                        "achievement": False
                                    },
                                    "gameFour": {
                                        "achievement": False
                                    },
                                    "gameFive": {
                                        "achievement": True
                                    }
                                }
                            }
                        ]
                    )
                ]),
            **common_minigame_status_codes
        }
    )
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        exclude=True
    )
    def retrieve(self, request, *args, **kwargs):
        pass

    @extend_schema(
        summary='Полученние информации о положении игрока в таблице лидеров',
        tags=['Liderboard'],
        description="""
            Инофрмация о положении игрока в таблице лидеров. Дополнительно список 100 лучших игроков по очкам.
            
            Параметр запроса:
                id - идентификатор игрока
                GET /api/v1/liderboard/{id}/ranking/
            """,
        request=PlayerSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=LeaderboardPlayerSerializer,
                description='Ответ получен',
                examples=[
                    OpenApiExample(
                        name='Список лидеров',
                        value=[{
                            "player_id": 42,
                            "place": 17,
                            "total_players": 54,
                            "liderdoard": [
                                {
                                    "name": "Top_player",
                                    "own_coins": 0,
                                    "own_money": 0,
                                    "top_score": 800,
                                    "achievement": {
                                            "gameOne": {
                                                "achievement": False
                                            },
                                        "gameTwo": {
                                                "achievement": False
                                            },
                                        "gameThree": {
                                                "achievement": False
                                            },
                                        "gameFour": {
                                                "achievement": False
                                            },
                                        "gameFive": {
                                                "achievement": False
                                            }
                                    },
                                }
                            ]
                        }]
                    )
                ]),
            **common_minigame_status_codes
        })
    @action(detail=True, methods=['get'], url_path='ranking')
    def get_player_leaderboard(self, request, pk=None):

        try:
            pk = int(pk)
        except ValueError:
            raise ValidationError("Player ID должен быть целым числом")

        try:
            player = Player.objects.get(id=pk)
        except Player.DoesNotExist:
            return Response({"error": "Player not found"}, status=404)

        queryset = self.get_queryset()
        serializer_board = self.serializer_class(queryset, many=True)

        players = Player.objects.order_by('-top_score')

        player_rank = list(players).index(player) + 1

        serializer_game = PlayerMinigameSerializer(
            player.playerminigame_set.all(), many=True)
        minigame_data = serializer_game.data

        achievement_count = sum(
            1 for game in minigame_data if game.get("achievement", False))

        response_data = {
            "player_id": player.id,
            "player_name": player.name,
            "place": player_rank,
            "achievement_count": achievement_count,
            "own_coins": player.own_coins,
            "top_score": player.top_score,
            "total_players": players.count(),
            "liderdoard": serializer_board.data
        }

        return Response(response_data)