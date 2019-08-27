from flask import Flask, render_template, request, jsonify

from db import close_db, init_db_command, insert_or_update_book, get_db
from spider import JiumoDiary

app = Flask(__name__)
app.teardown_appcontext(close_db)
app.cli.add_command(init_db_command)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/')
def search():
    keyword = request.args.get('keyword')
    results = []
    if keyword:
        db = get_db()
        rows = db.execute(
            "SELECT * FROM books WHERE title LIKE '%%%s%%'" % keyword)
        for row in rows:
            results.append(row)
        if not results:
            _results = JiumoDiary(keyword).results
            for item in _results:
                # print('-' * 40)
                # print(item)
                # print('-' * 40)
                for row in item.get('details', {}).get('data', []):
                    data = {
                        'title': row['title'],
                        'url': row['link'],
                        'description': row['des'],
                    }
                    results.append(data)
                    insert_or_update_book(**data)
    return render_template('index.html', results=results, keyword=keyword)
