import click
import sqlite3

from flask import g
from flask.cli import with_appcontext

def get_db():
    """使用flask g变量存储数据库连接

    :return:
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            'ebook.sqlite',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """关闭数据库操作
    从

    :param e:
    :return:
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


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


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')