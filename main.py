from http import HTTPStatus

from flask import Flask, abort, jsonify, request

from forms import SearchMoviesValidator, validation_errors_to_dict
from my_enums import SortOrder, SortField
from services import MoviesService

app = Flask('movies_service')
BASE_ELASTIC_URL = 'http://127.0.0.1:9200'


@app.route('/api/movies/<movie_id>', methods=['GET'])
def movie_details(movie_id: str):
    """
    Эндпоинт для получения детальной информации о фильме по его ID.
    """
    movie = MoviesService.get_movie_by_id(movie_id)
    if movie is None:
        abort(HTTPStatus.NOT_FOUND)
    return jsonify(movie.to_dict())


@app.route('/api/movies', methods=['GET'], strict_slashes=False)
def movies_list():
    """
    Эндпоинт для поиска фильмов по пользовательскому запросу
    """
    form = SearchMoviesValidator(request.args)
    validation_errors = []
    if not form.validate():
        validation_errors = validation_errors_to_dict(form.errors)

    if validation_errors:
        return jsonify(detail=validation_errors), HTTPStatus.UNPROCESSABLE_ENTITY

    movies = MoviesService.search_movies(
        search_query=form.search.data,
        sort_order=SortOrder(form.sort_order.data),
        sort=SortField(form.sort.data),
        page=form.page.data,
        limit=form.limit.data,
    )
    return jsonify([m.to_dict() for m in movies])


if __name__ == '__main__':
    app.run(port=8000)
