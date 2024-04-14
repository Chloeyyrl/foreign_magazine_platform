from flask import Flask, request, jsonify,session
import pymysql
import pymysql.cursors
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = "2a8cd348cbc2c74268c58af55e6dc767"


DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'db': 'foreign_magazine_data',
    'cursorclass': pymysql.cursors.DictCursor
}

@app.route('/')
def home():
    return 'Welcome to the API!'

@app.route('/api/check_reading_status', methods=['GET'])
def check_reading_status():
    user_id = request.args.get('userId')
    article_id = request.args.get('article_id')

    connection = pymysql.connect(**DATABASE_CONFIG)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `reading_status` WHERE `user_id`=%s AND `article_id`=%s"
            cursor.execute(sql, (user_id, article_id))
            article = cursor.fetchone()
            
            is_read = article is not None
            if is_read:
                return jsonify({"is_read": True}), 200
            else:
                return jsonify({"is_read": False}), 200
    except pymysql.MySQLError as e:
        return jsonify({"message": "数据库错误", "错误": str(e)}), 500
    finally:
        connection.close()


@app.route('/api/get_article', methods=['GET'])
def get_article():
    connection = pymysql.connect(**DATABASE_CONFIG)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `article`"
            cursor.execute(sql)
            articles = cursor.fetchall()
            return jsonify(articles), 200
    except pymysql.MySQLError as e:
        return jsonify({"message": "数据库错误", "错误": str(e)}), 500
    finally:
        connection.close()


@app.route('/api/login', methods=['POST'])
def login():
    # 获取请求数据
    data = request.json
    username = data['username']
    password = data['password']

    # 建立数据库连接
    connection = pymysql.connect(**DATABASE_CONFIG)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `user` WHERE `username` = %s AND `password` = %s"
            cursor.execute(sql, (username, password))
            user = cursor.fetchone()
            if user is not None:
                userid = user['id']
                return jsonify({"message": "登录成功!", "userid": userid, "username": username}), 200
            else:
                return jsonify({"message": "用户名或密码错误"}), 401
    except pymysql.MySQLError as e:
        return jsonify({"message": "数据库错误", "错误": str(e)}), 500
    finally:
        connection.close()

@app.route('/api/register', methods=['POST'])  
def register():  
    data = request.json
    username = data['username']
    password = data['password']
    
    connection = pymysql.connect(**DATABASE_CONFIG)
    try:
        with connection.cursor() as cursor:
            # 先检查用户名是否已存在
            check_sql = "SELECT * FROM `user` WHERE `username` = %s"
            cursor.execute(check_sql, (username,))
            if cursor.fetchone() is not None:
                return jsonify({"message": "该用户名已存在！"}), 400
            
            # 插入新用户
            insert_sql = "INSERT INTO `user` (`username`, `password`) VALUES (%s, %s)"
            cursor.execute(insert_sql, (username, password))
            connection.commit()
            return jsonify({"message": "注册成功!"}), 201
    except pymysql.MySQLError as e:
        return jsonify({"message": "数据库错误", "错误": str(e)}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
