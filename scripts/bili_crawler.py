#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
sys.path.append(os.path.dirname(__name__))

from datetime import datetime
import logging
import random
import time

import requests
from bs4 import BeautifulSoup

from app import create_app, db
from app.manga.models import Manga, Label, MangaLabelRef

app = create_app()

SAVE_INTO_DB = False


logging.basicConfig(level=logging.INFO)

BILI_MANGA_LIST_URL = ("https://bangumi.bilibili.com/media/web_api/search/result?"
                       "season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&"
                       "pub_date=-1&style_id=-1&order=3&st=1&sort=0&page={page_num}&season_type=1&pagesize=20")

BILI_MANGA_DETAIL_URL = "https://www.bilibili.com/bangumi/media/md{media_id}"


def get_manga_detail_data(media_id):
    """获取番剧详情页数据"""
    detail_url = BILI_MANGA_DETAIL_URL.format(media_id=media_id)
    logging.info("[get_mana_detail_data] start! media_id: %s" % media_id)

    time.sleep(random.random() * 0.1)
    for n in range(3):
        try:
            res = requests.get(detail_url, verify=False)
            res.raise_for_status()
            break
        except Exception as e:
            logging.error("get detail data error! %s, retry: %n", str(e), n+1)
            if n >= 2:
                return None
            # return None

    detail_data = {}
    bs = BeautifulSoup(res.text, features="html.parser")
    info_item = bs.find("div", class_="media-info-r")
    if info_item:
        # 标签
        detail_data["tag"] = [tag.text.strip() for tag in
                              info_item.find_all("span", class_="media-tag")]

        # 介绍
        detail_data["intro"] = res.text.split('evaluate":"')[-1].split('","long_review')[0].replace("\\n", "")

    logging.info("[get_manga_detail_data] success!")
    return detail_data


def get_manga_page_data(page_num):
    """获取分页番剧数据"""
    logging.info("[get_manga_page_data] start! page_num: %s" % page_num)
    page_url = BILI_MANGA_LIST_URL.format(page_num=page_num)

    try:
        res = requests.get(page_url, verify=False)
        res.raise_for_status()
    except Exception as e:
        logging.exception(e)
        return None

    json_data = res.json()
    data = json_data["result"]["data"]

    result_list = []
    for item in data:
        if "（僅限港澳地區）" in item["title"]:
            logging.warn("%s restricted!")
            continue

        if item["media_id"]:
            detail_data = get_manga_detail_data(item["media_id"])
            if not detail_data:
                # pass this item
                logging.error("get detail data failed! media_id: %s", item["media_id"])
                continue

            item.update(detail_data)

        result_list.append(item)

    logging.info("[get_manga_page_data] finish! page_num: %s, length: %s" % (page_num, len(result_list)))
    return result_list


def crawl_manga_list_data(max_page=2):
    """抓取番剧列表数据"""
    all_manga_list = []

    for page in range(1, max_page+1):
        data = get_manga_page_data(page)
        if data:
            all_manga_list.extend(data)

    logging.info("in total %s" % len(all_manga_list))

    # 保存抓取数据
    if SAVE_INTO_DB:
        save_manga_data(all_manga_list)
    return True


def get_format_timestr(ts):
    if not ts:
        return ""
    dt = datetime.fromtimestamp(ts)
    return datetime.strftime(dt, "%Y年%m月%d日")


def save_manga_data(manga_list):
    """保存漫画数据"""
    now = datetime.now()
    manga_label_map = {}  # manga_id: label_list

    # 保存番剧数据
    idx = 0
    for manga_item in manga_list:
        idx += 1
        new_obj = Manga(
            name=manga_item["title"],
            cover_url=manga_item["cover"],
            is_finished=manga_item["is_finish"],
            start_time=get_format_timestr(manga_item["order"].get("pub_date", 0)),
            update_time="",  # 暂不插入
            description=manga_item["intro"],
            bili_score=manga_item["order"].get("score", ""),
            create_time=now,
            modify_time=now,
            deleted=0)

        db.session.add(new_obj)
        db.session.flush()
        manga_label_map[new_obj.id] = manga_item["tag"] or []

        if idx and idx % 100 == 0:
            db.session.commit()

    db.session.commit()
    logging.info("save %s manga into db..." % idx)

    # 保存番剧标签数据
    label_map = {}
    for manga_id, label_list in manga_label_map.items():
        label_ids = []
        for label in label_list:
            # 保存新标签
            if label not in label_map:
                label_obj = Label(
                    name=label,
                    priority=0,
                    create_time=now,
                    modify_time=now,
                    deleted=0
                )

                db.session.add(label_obj)
                db.session.flush()
                label_map[label] = label_obj.id

            label_id = label_map.get(label) or 0
            if label_id:
                label_ids.append(int(label_id))

        # 保存番剧标签表
        if label_ids:
            for label_id in label_ids:
                db.session.add(MangaLabelRef(
                    manga_id=manga_id,
                    label_id=label_id,
                    create_time=now,
                    modify_time=now,
                    deleted=0
                ))

        db.session.commit()

    logging.info("save manga label into db...%s", len(manga_label_map))
    return True


if __name__ == "__main__":
    with app.app_context():
        crawl_manga_list_data(10)
