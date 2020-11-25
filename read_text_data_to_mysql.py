#!/usr/bin/python3
import re
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "test")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()

print("Database version : %s " % data)

f = open("./data.txt")  # 返回一个文件对象
line = f.readline()  # 调用文件的 readline()方法
buffer_size = 10000
buffer = []
count = 0

while line:
    line = f.readline()
    print(line)
    res = re.search(r'(?P<phone>\d+)\s*(?P<uid>\d+)\s*', line)
    if res is not None:
        phone = res.group('phone')  # 通过命名分组引用分组
        uid = res.group('uid')  # 通过命名分组引用分组
        buffer.append((uid, phone))
        # print(phone)
        # print(uid)

    if len(buffer) >= buffer_size:
        count += 1
        sql = 'insert into uid_phone(uid, phone) values (%s, %s)'
        try:
            cursor.executemany(sql, buffer)
            db.commit()
            print('===================已处理%d============' % (count * buffer_size))
            buffer = []

        except:
            print('插入数据异常，请重试')
            db.rollback()

if not line and len(buffer) > 0:
    sql = 'insert into uid_phone(uid, phone) values (%s, %s)'
    try:
        cursor.executemany(sql, buffer)
        db.commit()
        print('===================已处理%d============' % (count * buffer_size + len(buffer)))
        buffer = []

    except:
        print('插入数据异常，请重试')
        db.rollback()

f.close()

# 关闭数据库连接
db.close()
