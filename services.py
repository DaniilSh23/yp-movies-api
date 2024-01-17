from typing import Optional, List
from urllib.parse import urljoin

import requests

from settings import BASE_ELASTIC_URL, ELASTIC_PASSWD
from my_dataclasses import Movie, Actor, Writer, ShortMovie
from my_enums import SortField, SortOrder
from utils import make_request_session


class MoviesService:
    """
    Сервис с бизнес-логикой для фильмов.
    """

    @staticmethod
    def get_movie_by_id(movie_id: str) -> Optional[Movie]:
        """
        Получение филма по id
        """
        # Запрос к Elastic
        request_data = {
            'query': {
                'term': {
                    'id': {
                        'value': movie_id
                    }
                }
            }
        }
        session = make_request_session()
        response = session.get(
            url=urljoin(BASE_ELASTIC_URL, 'movies/_search'),
            json=request_data,
            headers={'Content-Type': 'application/json'},
            auth=("elastic", ELASTIC_PASSWD),
        )
        if not response.ok:
            response.raise_for_status()

        # Достаем результат запроса к ES
        data = response.json()
        result = data['hits']['hits']
        if not result:
            return None

        # Обработка и упаковка результата запроса
        movie_raw = result[0]['_source']
        movie = Movie(
            id=movie_raw['id'],
            title=movie_raw['title'],
            imdb_rating=movie_raw['imdb_rating'],
            description=movie_raw['description'],
            genre=movie_raw['genre'],
            actors=[Actor(**person) for person in movie_raw['actors']],
            writers=[Writer(**person) for person in movie_raw['writers']],
            directors=movie_raw['director']
        )
        return movie

    @staticmethod
    def search_movies(*, search_query: Optional[str] = None, sort_order: SortOrder = SortOrder.ASC,
                      sort: SortField = SortField.ID, page: int = 1, limit: int = 50) -> List[ShortMovie]:
        """
        Метод для поиска фильмов.
        """
        sort_value = sort.value
        if sort_value == SortField.TITLE.value:
            sort_value = f'{SortField.TITLE.value}.raw'

        # Запрос к ES
        request_data = {
            'size': limit,
            'from': (page - 1) * limit,
            'sort': [
                {
                    sort_value: sort_order.value
                }
            ],
            '_source': ['id', 'title', 'imdb_rating'],
        }
        if search_query:
            request_data['query'] = {
                'multi_match': {
                    'query': search_query,
                    'fuzziness': 'auto',
                    'fields': [
                        'title^5',
                        'description^4',
                        'genre^3',
                        'actors_names^3',
                        'writers_names^2',
                        'director'
                    ]
                }
            }
        session = make_request_session()
        response = session.get(
            url=urljoin(BASE_ELASTIC_URL, 'movies/_search'),
            json=request_data,
            headers={'Content-Type': 'application/json'},
            auth=("elastic", ELASTIC_PASSWD),
        )
        if not response.ok:
            response.raise_for_status()

        # Обрабатываем и упаковываем данные для ответа
        data = response.json()
        result = data['hits']['hits']
        movies = []

        if not result:
            return movies

        for record in result:
            movies.append(ShortMovie(
                id=record['_source']['id'],
                title=record['_source']['title'],
                imdb_rating=record['_source']['imdb_rating']
            ))
        return movies
