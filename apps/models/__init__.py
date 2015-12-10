# -*- coding: utf-8 -*-
# !/usr/bin/python

# 初始化数据库连接:
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test', convert_unicode=True)
# 创建DBSession类型:
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# Base = declarative_base()
# Base.query = db_session.query_property()
#
#
# def init_db():
#     # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在
#     # 元数据上。否则你就必须在调用 init_db() 之前导入它们。
#     import apps.models.models
#     Base.metadata.create_all(bind=engine)
