# -*- coding: UTF-8 -*-

from app import db

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Manga(db.Model):
    """番剧信息表"""
    __tablename__ = "manga"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    cover_url = Column(String(500))  # 封片图
    is_finished = Column(Integer)  # 状态: 0,连载中; 1,结束; 2,未开始;
    start_time = Column(String(50))  # 开始播放时间
    update_time = Column(String(50))  # 更新时间
    description = Column(Text)
    bili_score = Column(String(10))  # b站评分
    create_time = Column(DateTime)  # 数据创建时间
    modify_time = Column(DateTime)  # 数据更新时间
    deleted = Column(Integer, default=0)  # 状态: 0,正常; 1,删除

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cover_url": self.cover_url,
            "start_time": self.start_time,
            "update_time": self.update_time,
            "description": self.description,
            "bili_score": self.bili_score,
        }


class Label(db.Model):
    """标签表"""
    __tablename__ = "label"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    priority = Column(Integer)
    create_time = Column(DateTime)  # 数据创建时间
    modify_time = Column(DateTime)  # 数据更新时间
    deleted = Column(Integer, default=0)  # 状态: 0,正常; 1,删除


class MangaLabelRef(db.Model):
    """番剧标签关系表"""
    __tablename__ = "manga_label_ref"

    id = Column(Integer, primary_key=True)
    manga_id = Column(Integer, ForeignKey("manga.id"))
    label_id = Column(Integer, ForeignKey("label.id"))
    create_time = Column(DateTime)  # 数据创建时间
    modify_time = Column(DateTime)  # 数据更新时间
    deleted = Column(Integer, default=0)  # 状态: 0,正常; 1,删除

    label = relationship("Label")
