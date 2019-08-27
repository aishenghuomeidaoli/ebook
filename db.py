import sqlite3


def get_db():
    """获取生成数据库连接

    :return:
    """
    db = sqlite3.connect('ebook.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
    return db

def init_db():
    """数据库初始化表结构

    :return:
    """
    # 数据库表结构
    SQL_SCHEMA = """
DROP TABLE IF EXISTS books;

CREATE TABLE books(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  url TEXT NOT NULL,
  size INTEGER NULL,
  format TEXT NULL,
  description TEXT NULL
);
"""
    db = get_db()
    db.executescript(SQL_SCHEMA)
