drop database if exists news;
create database news;

drop table if exists news.comment;
create table news.comment(
    id int primary key auto_increment comment '主键',
    name varchar(255) comment '评论人',
    comment text comment '评论'
) comment '评论信息';

drop table if exists news.news;
create table news.news(
    id int primary key auto_increment comment '主键',
    title varchar(255) comment '标题',
    content text comment '内容',
    recommend_num varchar(255) comment '推荐数',
    comments_num varchar(255) comment '评论人数',
    view_num varchar(255) comment '浏览数',
    tag varchar(255) comment '标签',
    time varchar(255) comment '时间'
) comment '新闻信息'