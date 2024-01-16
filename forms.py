from typing import List

from wtforms import validators
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField
from wtforms.form import Form

from my_enums import SortField, SortOrder


class SearchMoviesValidator(Form):
    """
    Форма валидации данных для поиска фильмов.
    """
    limit = IntegerField('Limit', [validators.NumberRange(min=0)], default=50)
    page = IntegerField('Page', [validators.NumberRange(min=1)], default=1)
    search = StringField('Search', default='')
    sort = SelectField(
        'Sort',
        choices=[
            (SortField.ID.value, SortField.ID.value),
            (SortField.TITLE.value, SortField.TITLE.value),
            (SortField.IMDB_RATING.value, SortField.IMDB_RATING.value),
        ],
        default=SortField.ID.value,
    )
    sort_order = SelectField(
        'SortOrder',
        choices=[
            (SortOrder.ASC.value, SortOrder.ASC.value),
            (SortOrder.DESC.value, SortOrder.DESC.value),
        ],
        default=SortOrder.ASC.value,
    )


def validation_errors_to_dict(errors: dict) -> List[dict]:
    validation_errors = []
    for field_name, field_errors in errors.items():
        for err in field_errors:
            validation_errors.append(
                {
                    'loc': [
                        'query',
                        field_name,
                    ],
                    'msg': err
                },
            )
    return validation_errors
