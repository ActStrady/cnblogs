# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CnblogsItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 内容
    content = scrapy.Field()
    # 推荐数
    recommend_num = scrapy.Field()
    # 评论人数
    comments_num = scrapy.Field()
    # 浏览数
    view_num = scrapy.Field()
    # 标签
    tag = scrapy.Field()
    # 时间
    time = scrapy.Field()


class NewsDetailsItem(scrapy.Item):
    # 文章行
    line = scrapy.Field()


class NewsCommentItem(scrapy.Item):
    # 评价人
    name = scrapy.Field()
    # 评论
    comment = scrapy.Field()
