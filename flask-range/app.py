import os
import sqlite3
import subprocess
import urllib.parse
from functools import wraps

import jwt
import requests
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, send_from_directory, jsonify
)

app = Flask(__name__)
app.secret_key = "weak_secret_for_training_only"
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------------------------------------------------------
# 初始化 SQLite 数据库
# -------------------------------------------------------------------
def init_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    c = conn.cursor()
    c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)")
    c.execute("INSERT INTO users VALUES (1, 'admin', 'admin123', 'admin')")
    c.execute("INSERT INTO users VALUES (2, 'alice', 'alice123', 'user')")
    c.execute("INSERT INTO users VALUES (3, 'bob', 'bob123', 'user')")
    c.execute("CREATE TABLE profiles (id INTEGER PRIMARY KEY, user_id INTEGER, email TEXT, phone TEXT)")
    c.execute("INSERT INTO profiles VALUES (1, 1, 'admin@range.local', '13800000001')")
    c.execute("INSERT INTO profiles VALUES (2, 2, 'alice@range.local', '13800000002')")
    c.execute("INSERT INTO profiles VALUES (3, 3, 'bob@range.local', '13800000003')")
    conn.commit()
    return conn

DB_CONN = init_db()

def query_db(query, params=()):
    c = DB_CONN.cursor()
    c.execute(query, params)
    return c.fetchall()

# -------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")

# ===================================================================
# 1. SQL 注入
# ===================================================================
@app.route("/sqli/login", methods=["GET", "POST"])
def sqli_login():
    msg = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        try:
            result = query_db(query)
            if result:
                msg = f"登录成功！用户信息：{result[0]}"
            else:
                msg = "用户名或密码错误"
        except Exception as e:
            msg = f"SQL 错误：{e}"
    return render_template("sqli.html", msg=msg)

@app.route("/sqli/data", methods=["GET"])
def sqli_data():
    uid = request.args.get("id", "1")
    query = f"SELECT * FROM users WHERE id={uid}"
    try:
        rows = query_db(query)
    except Exception as e:
        rows = []
    return render_template("sqli_data.html", rows=rows, query=query)

# ===================================================================
# 2. XSS
# ===================================================================
STORED_XSS = []

@app.route("/xss/reflected", methods=["GET", "POST"])
def xss_reflected():
    name = ""
    if request.method == "POST":
        name = request.form.get("name", "")
    elif request.method == "GET":
        name = request.args.get("name", "")
    return render_template("xss_reflected.html", name=name)

@app.route("/xss/stored", methods=["GET", "POST"])
def xss_stored():
    if request.method == "POST":
        content = request.form.get("content", "")
        if content:
            STORED_XSS.append(content)
    return render_template("xss_stored.html", posts=STORED_XSS)

# ===================================================================
# 3. CSRF
# ===================================================================
CSRF_BALANCE = 5000

@app.route("/csrf/transfer", methods=["GET", "POST"])
def csrf_transfer():
    global CSRF_BALANCE
    msg = ""
    if request.method == "POST":
        amount = request.form.get("amount", "0")
        CSRF_BALANCE -= int(amount)
        msg = f"转账成功！转账金额：{amount}"
    return render_template("csrf_transfer.html", balance=CSRF_BALANCE, msg=msg)

# ===================================================================
# 4. SSRF
# ===================================================================
@app.route("/ssrf/fetch", methods=["GET", "POST"])
def ssrf_fetch():
    content = ""
    error = ""
    if request.method == "POST":
        url = request.form.get("url", "")
        try:
            resp = requests.get(url, timeout=5)
            content = resp.text[:2000]
        except Exception as e:
            error = str(e)
    return render_template("ssrf_fetch.html", content=content, error=error)

# ===================================================================
# 5. 命令注入
# ===================================================================
@app.route("/rce/ping", methods=["GET", "POST"])
def rce_ping():
    output = ""
    if request.method == "POST":
        ip = request.form.get("ip", "")
        result = os.popen(f"ping -n 2 {ip}").read()
        output = result
    return render_template("rce_ping.html", output=output)

# ===================================================================
# 6. 文件上传
# ===================================================================
@app.route("/upload", methods=["GET", "POST"])
def file_upload():
    msg = ""
    file_url = ""
    if request.method == "POST":
        f = request.files.get("file")
        if f and f.filename:
            path = os.path.join(UPLOAD_FOLDER, f.filename)
            f.save(path)
            file_url = f"/uploads/{f.filename}"
            msg = "上传成功！"
    return render_template("upload.html", msg=msg, file_url=file_url)

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# ===================================================================
# 7. JWT 伪造
# ===================================================================
JWT_SECRET = "secret"

@app.route("/jwt/login", methods=["GET", "POST"])
def jwt_login():
    if request.method == "POST":
        username = request.form.get("username", "guest")
        role = "user"
        if username == "admin":
            role = "admin"
        token = jwt.encode({"username": username, "role": role}, JWT_SECRET, algorithm="HS256")
        session["jwt"] = token
        return redirect(url_for("jwt_admin"))
    return render_template("jwt_login.html")

@app.route("/jwt/admin")
def jwt_admin():
    token = request.args.get("token") or session.get("jwt")
    if not token:
        return "请先登录"
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except Exception as e:
        return f"Token 无效：{e}"
    if payload.get("role") != "admin":
        return f"权限不足。你的角色：{payload.get('role')}，需要 admin。Payload：{payload}"
    return f"恭喜，你已进入管理后台！Payload：{payload}"

# ===================================================================
# 8. IDOR
# ===================================================================
@app.route("/idor/profile")
def idor_profile():
    uid = request.args.get("user_id", "1")
    rows = query_db("SELECT * FROM profiles WHERE id=?", (uid,))
    if not rows:
        return "用户不存在"
    r = rows[0]
    # profiles: id(0), user_id(1), email(2), phone(3)
    return render_template("idor_profile.html", user_id=r[1], email=r[2], phone=r[3])

# ===================================================================
# 9. 不安全反序列化
# ===================================================================
import base64
import pickle

@app.route("/pickle", methods=["GET", "POST"])
def unsafe_pickle():
    result = ""
    if request.method == "POST":
        data = request.form.get("data", "")
        try:
            obj = pickle.loads(base64.b64decode(data))
            result = f"反序列化结果：{obj}"
        except Exception as e:
            result = f"错误：{e}"
    return render_template("pickle.html", result=result)

# ===================================================================
# 10. 日志记录
# ===================================================================
@app.after_request
def log_request(response):
    method = request.method
    path = request.path
    params = dict(request.args) or dict(request.form) or "(none)"
    print(f"[TRAFFIC] {method} {path} | params={params} | status={response.status_code}")
    return response

# -------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 50)
    print("Flask 靶场启动完成")
    print("地址：http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, host="127.0.0.1", port=5000)
