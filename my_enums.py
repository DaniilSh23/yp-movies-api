from enum import Enum


class SortOrder(Enum):
    ASC = 'asc'
    DESC = 'desc'


class SortField(Enum):
    ID = 'id'
    TITLE = 'title'
    IMDB_RATING = 'imdb_rating'
    