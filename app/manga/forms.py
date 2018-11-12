# -*- coding: UTF-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length

from app.manga.models import Manga


class MangaListForm(FlaskForm):
    page_num = IntegerField(validators=[DataRequired(), NumberRange(min=1)])
    page_size = IntegerField(validators=[DataRequired(), NumberRange(min=1)])


class MangaDetailForm(FlaskForm):
    manga_id = IntegerField(validators=[DataRequired(), NumberRange(min=1)])

    def validate(self, *args, **kw):
        result = super(FlaskForm, MangaDetailForm).validate(self, *args, **kw)
        if not result:
            return False

        manga = Manga.query.get(self.manga_id.data)
        if not manga or manga.deleted:
            self.errors["manga_id"] = "manga id is invalid!"
            return False

        return True


class MangaSearchForm(FlaskForm):
    keyword = StringField(validators=[DataRequired(), Length(min=1, max=5)])
