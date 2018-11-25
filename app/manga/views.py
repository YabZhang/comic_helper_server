# -*- coding: UTF-8 -*-

from flask import request, jsonify

from app.manga import manga
from app.manga.forms import MangaListForm, MangaDetailForm, MangaSearchForm
from app.manga.services import (
    get_manage_list, get_manga_detail, get_hot_manga_list, do_manga_search
)


@manga.route("/manga_list", methods=["GET"])
def manga_list():
    """番剧列表接口"""
    status_code = 200
    form = MangaListForm(request.args, csrf_enabled=False)

    if form.validate():
        page_num = form.page_num.data
        page_size = form.page_size.data
        result = get_manage_list(page_num, page_size)
    else:
        status_code = 400
        result = {"error": form.errors}

    return jsonify(result), status_code


@manga.route("/hot_manga_list", methods=["GET"])
def hot_manga_list():
    """热门番剧列表"""
    top_n = request.args.get("top_n", 10, type=int)
    result = get_hot_manga_list(top_n)
    return jsonify(result)


@manga.route("/manga_search", methods=["GET"])
def manga_search():
    """番剧搜索接口"""
    status_code = 200
    form = MangaSearchForm(request.args, csrf_enabled=False)

    if form.validate():
        keyword = form.keyword.data
        result = do_manga_search(keyword)
    else:
        status_code = 400
        result = {"error": form.errors}

    return jsonify(result), status_code


@manga.route("/manga_detail", methods=["GET"])
def manga_detail():
    """番剧详细信息接口"""
    status_code = 200
    form = MangaDetailForm(request.args, csrf_enabled=False)

    if form.validate():
        manga_id = form.manga_id.data
        result = get_manga_detail(manga_id)
    else:
        status_code = 400
        result = {"error": form.errors}

    return jsonify(result), status_code
