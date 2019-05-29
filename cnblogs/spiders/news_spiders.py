#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# @Time : 2019/5/28 15:42
# @Author : ActStrady@tom.com
# @FileName : news_spiders.py
# @GitHub : https://github.com/ActStrady/cnblogs
import re

from scrapy import Spider, Request
from cnblogs.items import CnblogsItem, NewsDetailsItem, NewsCommentItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class NewsSpider(Spider):
    name = 'news'

    def start_requests(self):
        yield Request('https://news.cnblogs.com/')

    def parse(self, response):
        item = CnblogsItem()
        news_list = response.xpath("//div[@class='news_block']")
        for news in news_list:
            # 标题
            title = news.xpath(".//h2[@class='news_entry']/a/text()").extract_first().strip()
            item['title'] = title
            # 内容
            content = news.xpath(".//div[@class='entry_summary']/text()").extract()
            # 有的内容会有前面的其他标签
            for cont in content:
                cont = cont.strip()
                # 把没内容的第一条过滤掉
                if cont != '':
                    content = cont
            item['content'] = content
            # 推荐数
            recommend_num = news.xpath(".//div[@class='diggit']/span/text()").extract_first().strip()
            item['recommend_num'] = recommend_num
            # 评论人数
            comments_num = news.xpath(".//span[@class='comment']/a/text()").extract_first().strip()
            comments_num = re.findall('\\d', comments_num)[0]
            item['comments_num'] = comments_num
            # 浏览数
            view_num = news.xpath(".//span[@class='view']/text()").extract_first().strip()
            view_num = re.findall('\\d', view_num)[0]
            item['view_num'] = view_num
            # 标签
            tag = news.xpath(".//span[@class='tag']/a/text()").extract()
            item['tag'] = tag
            # 时间
            time = news.xpath(".//span[@class='gray']/text()").extract_first().strip()
            item['time'] = time
            yield item
        # 处理下一页
        next_text = response.xpath("//div[@class='pager']/a[last()]/text()").extract_first().strip()
        print(next_text)
        next_url = response.xpath("//div[@class='pager']/a[last()]/@href").extract()
        if next_text == 'Next >':
            # 当前url加上参数url
            next_url = response.urljoin(next_url[0])
            # 关掉过滤
            yield Request(next_url, dont_filter=True)

    # TODO 爬取所有文章内容和评论
    def news_text_parse(self, response):
        news_item = NewsDetailsItem()
        comment_item = NewsCommentItem()
        news = response.xpath("//div[@id='news_body']/p/text()").extract()
        for line in news:
            news_item['line'] = line.strip('\u3000')
            yield news_item

        names = response.xpath("//a[@class='comment-author']/text()").extract()
        comments = response.xpath("//div[@class='comment_main']/text()[last()]").extract()
        # 评论数据
        for i in range(len(comments)):
            comment_item['name'] = names[i]
            comment_item['comment'] = comments[i]
            yield comment_item


class NewsDetailsSpider(Spider):
    name = 'news_details'

    # 初始化，定义selenium driver
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 将Chrome不弹出界面，实现无界面爬取
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def start_requests(self):
        yield Request('https://news.cnblogs.com/n/625986/')

    def parse(self, response):
        news_item = NewsDetailsItem()
        comment_item = NewsCommentItem()
        news = response.xpath("//div[@id='news_body']/p/text()").extract()
        for line in news:
            news_item['line'] = line.strip('\u3000')
            yield news_item

        names = response.xpath("//a[@class='comment-author']/text()").extract()
        comments = response.xpath("//div[@class='comment_main']/text()[last()]").extract()
        # 评论数据
        for i in range(len(comments)):
            comment_item['name'] = names[i]
            comment_item['comment'] = comments[i]
            yield comment_item
