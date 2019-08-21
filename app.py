from flask import Flask, render_template

from db import close_db, init_db_command, get_db

app = Flask(__name__)
app.teardown_appcontext(close_db)
app.cli.add_command(init_db_command)


@app.route('/')
def index():
    db = get_db()
    rows = db.execute("select * from books")
    return render_template('index.html', rows=rows)
