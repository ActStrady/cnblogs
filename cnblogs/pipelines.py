# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from cnblogs.items import NewsCommentItem, NewsDetailsItem
from util import mysql_util


class CnblogsPipeline(object):
    def process_item(self, item, spider):
        # 判定item
        if isinstance(item, NewsDetailsItem):
            with open('news/a.txt', 'a', encoding='utf-8') as f:
                f.writelines(item['line'] + '\n')
        return item


class CommentPipeline(object):
    def __init__(self):
        # 获取mysql连接
        self.db_conn = mysql_util.get_mysql_connect()
        # 获取mysql游标
        self.db_cursor = self.db_conn.cursor()

    def open_spider(self, spider):
        # 清空表
        self.db_cursor.execute('truncate news.comment')
        # 执行news时清空表
        if spider.name == 'news':
            self.db_cursor.execute('truncate news.news')

    def process_item(self, item, spider):
        # 判定item
        if isinstance(item, NewsCommentItem):
            sql = '''
                insert into news.comment(name, comment)
                values(%s, %s)
            '''
            comment = (item['name'], item['comment'])
            self.db_cursor.execute(sql, comment)
        if spider.name == 'news':
            sql_news = '''
                insert into news.news(title, content, recommend_num, comments_num, view_num, tag, time)
                values(%s, %s, %s, %s, %s, %s, %s)
            '''
            news = (item['title'], item['content'], item['recommend_num'],
                    item['comments_num'], item['view_num'], str(item['tag']), item['time'])
            print(news)
            self.db_cursor.execute(sql_news, news)
        return item

    # 爬虫全部完成后执行一次（收尾工作）
    def close_spider(self, spider):
        # 提交
        self.db_conn.commit()
        # 关闭
        self.db_cursor.close()
        self.db_conn.close()
