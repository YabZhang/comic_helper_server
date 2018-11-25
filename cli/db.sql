# `comic-helper` database
create database `comic-helper` character set utf8mb4 collate utf8mb4_unicode_ci;

# change to new db
use `comic-helper`;

# `manga` table
CREATE TABLE `manga` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
  `name` varchar(100) NOT NULL COMMENT '名称',
  `cover_url` varchar(500) NOT NULL COMMENT '图片链接',
  `is_finished` tinyint(4) NOT NULL COMMENT '# 状态: 0,连载中; 1,结束; 2,未开始;',
  `start_time` varchar(50) NOT NULL DEFAULT '' COMMENT '开始播放时间',
  `update_time` varchar(50) NOT NULL DEFAULT '' COMMENT '更新时间',
  `description` text,
  `bili_score` varchar(10) NOT NULL DEFAULT '未评分' COMMENT 'b站评分',
  `create_time` datetime NOT NULL COMMENT '数据创建时间',
  `modify_time` datetime NOT NULL COMMENT '数据更新时间',
  `deleted` tinyint(4) NOT NULL DEFAULT 0 COMMENT '状态: 0,正常; 1,删除'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='动漫相册';

# `label` table
CREATE TABLE `label` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
  `name` varchar(100) NOT NULL COMMENT '名称',
  `priority` int(11) NOT NULL DEFAULT '0' COMMENT '优先级',
  `create_time` datetime NOT NULL COMMENT '数据创建时间',
  `modify_time` datetime NOT NULL COMMENT '数据更新时间',
  `deleted` tinyint(4) NOT NULL DEFAULT 0 COMMENT '状态: 0,正常; 1,删除'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='标签';

# `manga_label_ref` table
CREATE TABLE `manga_label_ref` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
  `manga_id` int(11) NOT NULL COMMENT 'manga id',
  `label_id` int(11) NOT NULL COMMENT 'label id',
  `create_time` datetime NOT NULL COMMENT '数据创建时间',
  `modify_time` datetime NOT NULL COMMENT '数据更新时间',
  `deleted` tinyint(4) NOT NULL DEFAULT 0 COMMENT '状态: 0,正常; 1,删除'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='动漫标签关系';
