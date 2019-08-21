from flask import Flask, render_template

from db import close_db, init_db_command

app = Flask(__name__)
app.teardown_appcontext(close_db)
app.cli.add_command(init_db_command)


@app.route('/')
def index():
    return render_template('index.html')
