from flask import Flask, render_template, request, jsonify

from db import close_db, init_db_command, get_db
from spider import JiumoDiary

app = Flask(__name__)
app.teardown_appcontext(close_db)
app.cli.add_command(init_db_command)


@app.route('/')
def index():
    db = get_db()
    rows = db.execute("SELECT * FROM books")
    return render_template('index.html', rows=rows)


@app.route('/search/')
def search():
    keyword = request.args.get('keyword')
    results = []
    if keyword:
        results = JiumoDiary(keyword).results
    return render_template('index.html', results=results, keyword=keyword)
