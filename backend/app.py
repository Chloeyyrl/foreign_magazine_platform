from flask import Flask, request, jsonify,session
import pymysql
import pymysql.cursors
from flask_cors import CORS
from gpt_resp import call_gpt
import json
import re


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

#抽取生词和短语
@app.route('/api/extract_words_and_phrases', methods=['GET'])
def extract_words_and_phrases():
    article_id = request.args.get('article_id')
    user_id = request.args.get('user_id')
    print("两个id",article_id,user_id)
    connection = pymysql.connect(**DATABASE_CONFIG)
    try:
        with connection.cursor() as cursor:
            # 调用GPT抽取难词和短语
            sql = "SELECT * FROM `article` WHERE `id`=%s"
            cursor.execute(sql, (article_id,))
            article = cursor.fetchone()

            art_text = article['art_text']
            role_setting = 'You are an AI with excellent language skills and extensive reading of various foreign magazines. Your goal is to help users better understand the text.'
            prompt = f'''
                Your task is to perform the following actions:
                1 - Extract the difficult words, culturally loaded terms, and important phrases from the text, enclosed by <>, especially those words that are difficult to understand for non-native speakers.
                2 - Provide a brief and short definition or explanation of the extracted terms or phrases according to the context, no more than 20 words.
                3 - Format the output as a list of dictionaries, where each dictionary contains two key-value pairs: "term" and "definition". Ensure each term and its corresponding definition are enclosed in a separate dictionary. The list should look like this:
                    [
                        {{"term": "the word or phrase extracted", "definition": "the definition or explanation of the word or phrase"}},
                        {{"term": "another word or phrase extracted", "definition": "its definition or explanation"}}
                    ]
                <{art_text}>
            '''
            extract_result = call_gpt(role_setting, prompt)
            print("extract_result:",extract_result)
            
            try:
                term_list = json.loads(extract_result)
                # 遍历json_data中的每个条目
                for item in term_list:
                    term = item['term']
                    definition = item['definition'] 

                    insert_sql = "INSERT INTO `vocabulary` (`user_id`, `article_id`, `term`, `definition`) VALUES (%s, %s, %s, %s)"
                    cursor.execute(insert_sql, (user_id, article_id, term, definition))
                    print("单词或短语插入成功")

                return jsonify({"message":"单词和短语插入成功"}), 200
            except json.JSONDecodeError as e:
                return jsonify({"message": "结果解析错误", "错误": str(e)}), 500
        
    except pymysql.MySQLError as e:
        return jsonify({"message": "数据库错误", "错误": str(e)}), 500
    finally:
        connection.close()

#展示文章详情
@app.route('/api/get_article_info', methods=['GET'])
def get_article_info():
    article_id = request.args.get('article_id')

    connection = pymysql.connect(**DATABASE_CONFIG)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `article` WHERE `id`=%s"
            cursor.execute(sql, (article_id,))
            article = cursor.fetchone()
            return jsonify(article), 200
    except pymysql.MySQLError as e:
        return jsonify({"message": "数据库错误", "错误": str(e)}), 500
    finally:
        connection.close()

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
