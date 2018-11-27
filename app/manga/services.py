# -*- coding: UTF-8 -*-

from app import redis_cache
from app.manga.models import Manga, MangaLabelRef

from utils.base import cached

cache = redis_cache["DEFAULT"]

HOT_MANGE_ZSET = "hot_manga_zset"


@cached(3600*12)
def get_manga_labels(manga_id):
    manga_label_refs = MangaLabelRef.query \
        .filter(MangaLabelRef.deleted == 0) \
        .filter(MangaLabelRef.manga_id == manga_id) \
        .order_by(MangaLabelRef.create_time.desc()) \
        .all()

    label_names = []
    for ref in manga_label_refs:
        label = ref.label
        if label and not label.deleted:
            label_names.append(label.name)
    return label_names


@cached(3600)
def get_manage_list(page_num, page_size):
    """获取番剧列表数据"""

    query = Manga.query.filter(Manga.deleted == 0) \
        .order_by(Manga.create_time.desc())
    offset_ = page_size * (page_num - 1)
    items = query.limit(page_size).offset(offset_)

    data_list = []
    for item in items:
        item_dict = item.to_dict()
        item_dict["labels"] = get_manga_labels(item.id)
        data_list.append(item_dict)

    return data_list


@cached(600)
def get_manga_dict_by_ids(manga_ids):
    mangas = Manga.query.filter(Manga.deleted == 0) \
        .filter(Manga.id.in_(manga_ids)).all()
    return {manga.id: manga.to_dict() for manga in mangas}


def get_hot_manga_list(n=10):
    """返回最热门的番剧列表"""
    manga_ids = cache.zrevrange(HOT_MANGE_ZSET, 0, n-1)
    manga_ids = [int(manga_id) for manga_id in manga_ids]

    manga_list = []
    manga_dict = get_manga_dict_by_ids(manga_ids)

    for manga_id in manga_ids:
        manga_dat = manga_dict.get(int(manga_id))
        if manga_dat:
            manga_list.append(manga_dat)

    return manga_list


def do_manga_search(keyword):
    """搜索番剧"""
    # 默认返回前10条数据
    items = Manga.query.filter(Manga.deleted == 0) \
        .filter(Manga.name.startswith(keyword, autoescape=True)) \
        .limit(10)

    data_list = []
    for item in items:
        item_dict = item.to_dict()
        item_dict["labels"] = get_manga_labels(item.id)
        data_list.append(item_dict)

    return data_list


def add_hot_manga_score(manga_id):
    """增加热门评分"""
    cache.zincrby(HOT_MANGE_ZSET, manga_id, 1)


def get_manga_detail(manga_id):
    """获取番剧详情数据(包括标签，收藏)"""

    data = get_manga_dict_by_ids([manga_id]).get(manga_id)

    # 获取标签数据
    labels = get_manga_labels(manga_id)
    data["labels"] = labels

    # 增加热门计数
    add_hot_manga_score(manga_id)

    return data
