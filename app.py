from flask import Flask, render_template, request, redirect, url_for

from db import get_db

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        db = get_db()
        keyword = request.args.get('keyword', '')

        # 查询数据库，按 id 倒序排列，即新添加的记录优先显示；只显示20条
        if keyword:
            # 如果有关键字传入则使用关键字搜索 title 字段，如：
            # SELECT * FROM books WHERE title LIKE '%python%' LIMIT 20
            rows = db.execute(
                "SELECT * FROM books WHERE title LIKE '%%%s%%' ORDER BY id "
                "LIMIT 20" % keyword)
        else:
            rows = db.execute("SELECT * FROM books ORDER BY id DESC LIMIT 20")

        results = []
        for row in rows:
            results.append(row)
        return render_template('index.html', results=results, keyword=keyword)
    else:
        title = request.form.get('title')
        url = request.form.get('url')
        size = request.form.get('size', 0)
        fmt = request.form.get('format', '')
        description = request.form.get('description', '')

        # title，url 属于必填字段，这里进行校验；如果参数不全，则渲染提示信息
        if not title or not url:
            return render_template(
                'index.html', form=request.form, msg=u'标题或URL不能为空')

        # 校验完成后进行插入操作
        db = get_db()
        db.execute(
            "INSERT INTO books (title, url, size, format, description) "
            "VALUES ('%s', '%s', '%s', '%s', '%s')"
            % (title, url, size, fmt, description))
        db.commit()

        # 插入完成后，重定向至首页；浏览器会自动以 GET 请求访问 首页
        # return redirect('/')
        return redirect(url_for('index'))
