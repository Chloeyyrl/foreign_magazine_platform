from flask import Flask, request, jsonify,session
import pymysql
import pymysql.cursors
from flask_cors import CORS
from gpt_resp import call_gpt
import json
from datetime import datetime
import re
import secrets
from pdfquery import PDFQuery
import fitz  # PyMuPDF
from bs4 import BeautifulSoup
from tts_test import text_to_speech


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

def extract_text_with_formatting(pdf_path):
    doc = fitz.open(pdf_path)
    text = '<div>'
    for page in doc:
        blocks = page.get_text("dict")['blocks']
        for block in blocks:
            if 'lines' in block:
                for line in block['lines']:
                    for span in line['spans']:
                        
                        formatted_text = span['text']
                        style_attributes = []

                        # Adjust font size
                        font_size = span['size']
                        style_attributes.append(f"font-size: {font_size+4}px;")

                        # Check for bold
                        if span['flags'] & (1 << 4):
                            formatted_text = f"<b>{formatted_text}</b>"
                        # Check for italic
                        if span['flags'] & 2:
                            formatted_text = f"<i>{formatted_text}</i>"
                        # Check for superscript
                        if span['flags'] & (1 << 0):
                            formatted_text = f"<sup style='color: blue;'>{formatted_text}</sup>"
                            
                        style = ' '.join(style_attributes)
                        formatted_text = f"<span style='{style}'>{formatted_text}</span>"

                        text += formatted_text + ' '
                    text += '</br>'
        text += '</br>'
    return text


# 修改阅读状态
@app.route('/api/finish_reading', methods=['POST'])
def finish_reading():
    user_id = request.json['user_id']
    article_id = request.json['article_id']
    print('user_id:',user_id)
    print(user_id, article_id)
    connection = pymysql.connect(**DATABASE_CONFIG)
    # 先查询是否已经存在，再插入
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `reading_status` WHERE `user_id`=%s AND `article_id`=%s"
            cursor.execute(sql, (user_id, article_id))
            if cursor.fetchone() is not None:
                return jsonify({"message": "已经阅读过"}), 200

            insert_sql = "INSERT INTO `reading_status` (`user_id`, `article_id`) VALUES (%s, %s)"
            cursor.execute(insert_sql, (user_id, article_id))
            connection.commit()
            return jsonify({"message": "修改阅读状态成功"}), 201
    except pymysql.MySQLError as e:
        return jsonify({"message": "数据库错误", "错误": str(e)}), 500
    finally:
        connection.close()



#上传文件
@app.route('/api/upload', methods=['POST'])
def upload():
    title = request.form.get('title')
    category = request.form.get('category')
    uploaded_by = request.form.get('userid')
    source = request.form.get('source')

    update_time = datetime.now().date().strftime('%Y-%m-%d') #字符串格式
    file = request.files['file']
    current_date = datetime.now().strftime('%Y%m%d')
    clean_filename = file.filename.replace(' ', '_')
    random_string = secrets.token_hex(4)  
    filename = f"{current_date}_{random_string}_{clean_filename}"

    #print(filename)
    save_path = f'./pdfs/{filename}'
    # 保存文件
    file.save(save_path)
    
    content = extract_text_with_formatting(save_path)
    soup = BeautifulSoup(content, 'html.parser')

    # 获取纯文本，去除所有HTML标签
    art_text = soup.get_text()
    audio_filepaths = text_to_speech(art_text)

    

    connection = pymysql.connect(**DATABASE_CONFIG)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `article` (`title`, `category`, `content`,`art_text`,`article_source`,`uploaded_by`,`update_time`,`audio_path`) VALUES (%s, %s, %s, %s, %s,%s, %s,%s)"
            cursor.execute(sql, (title, category, content, art_text, source, uploaded_by, update_time,audio_filepaths))
            connection.commit()
            return jsonify({"message": "文章上传成功"}), 201
    except pymysql.MySQLError as e:
        return jsonify({"message": "数据库错误", "错误": str(e)}), 500
    finally:
        connection.close()

#聊天框
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No message provided"}), 400
    dialogue_history = data['dialogue_history']
    # analyzed_sentence = data['sentence']
    role_setting = "You are an AI with excellent language skills and can answer questions precisely."
    
    user_question = f'''
        User: {data['msg']}
    '''
    #prompt += user_question
    prompt = user_question + dialogue_history
    print('对话历史:',dialogue_history)
    print('---------------------------------------------------------------------------')
    answer = call_gpt(role_setting, prompt)
    return jsonify({"answer": answer}), 200

#语法分析
@app.route('/api/analyze_grammar', methods=['POST'])
def alynaze_grammar():
    sentence = request.get_json()
    if not sentence:
        return jsonify({"error": "No sentence provided"}), 400
    role_setting = 'You are an AI with excellent language skills and extensive reading of various foreign magazines. Your goal is to help users better understand the text.'
    
    prompt = f'''Your task is to perform the following actions:
    1 - Analyze the provided sentence to explain its grammatical structure
    2 - Provide a detailed explaination of this sentence
    3 - Output the result in html format. The result should look like this:
        <html>
            <h3>Original Sentence:</h2>
            <h3>Grammar Analysis:</h2>
            <h3>Detailed Explanation:</h2>
        </html>
    Provided sentence: {sentence['sentence']}
    '''
 

    grammar_analysis = call_gpt(role_setting, prompt)
    return jsonify({"grammar_analysis": grammar_analysis,'analyze_grammar_prompt':prompt}), 200
    

#添加新的一行
@app.route('/api/add_term', methods=['GET'])
def add_term():
    user_id = request.args.get('user_id')
    article_id = request.args.get('article_id')
    term = request.args.get('term')
    definition = request.args.get('definition')
    if not term or not definition:
        return jsonify({"message": "term和definition不能为空"}), 400
    else:
        connection = pymysql.connect(**DATABASE_CONFIG)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `vocabulary` (`user_id`, `article_id`, `term`, `definition`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (user_id, article_id, term, definition))
                connection.commit()
                return jsonify({"message": "添加成功"}), 201
        except pymysql.MySQLError as e:
            return jsonify({"message": "数据库错误", "错误": str(e)}), 500
        finally:
            connection.close()

#删除
@app.route('/api/delete_term', methods=['GET'])
def delete_term():
    id = request.args.get('id')
    # print("id",id)
    connection = pymysql.connect(**DATABASE_CONFIG)
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `vocabulary` WHERE `id`=%s"
            cursor.execute(sql, (id, ))
            # print(cursor.execute(sql, (id, )))
            connection.commit()
            return jsonify({"message": "删除成功"}), 200
    except pymysql.MySQLError as e:
        return jsonify({"message": "数据库错误", "错误": str(e)}), 500
    finally:
        connection.close()


#展示生词和短语
@app.route('/api/show_words_and_phrases', methods=['GET'])
def show_words_and_phrases():
    user_id = request.args.get('user_id')
    article_id = request.args.get('article_id')

    connection = pymysql.connect(**DATABASE_CONFIG)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `vocabulary` WHERE `user_id`=%s AND `article_id`=%s"
            cursor.execute(sql, (user_id, article_id))
            words_and_phrases = cursor.fetchall()

            if not words_and_phrases:
                return jsonify({"is_disabled":False}), 200
            else:
                return jsonify({"is_disabled":True,"words_and_phrases":words_and_phrases}), 200
    except pymysql.MySQLError as e:
        return jsonify({"message": "数据库错误", "错误": str(e)}), 500
    finally:
        connection.close()
    
#抽取生词和短语
@app.route('/api/extract_words_and_phrases', methods=['GET'])
def extract_words_and_phrases():
    article_id = request.args.get('article_id')
    user_id = request.args.get('user_id')
    # 判断两个参数是否为空
    if not article_id and not user_id:
        print("参数为空")
    connection = pymysql.connect(**DATABASE_CONFIG)
    try:
        with connection.cursor() as cursor:
            # 调用GPT抽取难词和短语
            sql = "SELECT * FROM `article` WHERE `id`=%s "
            cursor.execute(sql, (article_id,))
            article = cursor.fetchone()

            art_text = article['art_text']
            role_setting = 'You are an AI with excellent language skills and extensive reading of various foreign magazines. Your goal is to help users better understand the text.'
            prompt = f'''
                Your task is to perform the following actions:
                1 - Extract the difficult words, culturally loaded terms, and important phrases from the text, which is enclosed by <>, especially those words that are difficult to understand for non-native speakers.
                2 - Provide a brief and short definition or explanation of the extracted terms or phrases according to the context, no more than 20 words.
                3 - Format the output as a list of dictionaries, where each dictionary contains two key-value pairs: "term" and "definition". Ensure each term and its corresponding definition are enclosed in a separate dictionary. The list should look like this:
                    [
                        {{"term": "the word or phrase extracted", "definition": "the definition or explanation of the word or phrase"}},
                        {{"term": "another word or phrase extracted", "definition": "its definition or explanation"}}
                    ]
                <{art_text}>
            '''
            extract_result = call_gpt(role_setting,prompt)
            print(extract_result)
    
            try:
                term_list = json.loads(extract_result)
                # print("term_list",term_list,type(term_list))
                # 遍历json_data中的每个条目
                for item in term_list:
                    term = item['term']
                    definition = item['definition'] 
                    # print("term----",term)
                    # print("definition---",definition)

                    insert_sql = "INSERT INTO `vocabulary` (`user_id`, `article_id`, `term`, `definition`) VALUES (%s, %s, %s, %s)"
                    cursor.execute(insert_sql, (user_id, article_id, term, definition))
                    print(f"{term}插入成功")

                return jsonify({"message":"抽取的单词和短语成功保存到数据表"}), 200
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
    user_id = request.args.get('user_id')

    connection = pymysql.connect(**DATABASE_CONFIG)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `article` WHERE `id`=%s"
            cursor.execute(sql, (article_id,))
            article = cursor.fetchone()
            highlighted_terms_sql = "SELECT `term` FROM `vocabulary` WHERE `article_id`=%s AND `user_id`=%s"
            cursor.execute(highlighted_terms_sql, (article_id, user_id))
            highlighted_terms = cursor.fetchall()
            
            return jsonify({'article':article,'highlighted_terms':highlighted_terms}), 200
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

@app.route('/api/get_article_user_uploaded', methods=['GET'])
def get_article_user_uploaded():
    user_id = request.args.get('userId')

    connection = pymysql.connect(**DATABASE_CONFIG)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `article` WHERE `uploaded_by`=%s" #查询用户上传的文章
            cursor.execute(sql, (user_id,))
            articles = cursor.fetchall()
            return jsonify(articles), 200
    except pymysql.MySQLError as e:
        return jsonify({"message": "数据库错误", "错误": str(e)}), 500
    finally:
        connection.close()

@app.route('/api/get_article', methods=['GET'])
def get_article():

    connection = pymysql.connect(**DATABASE_CONFIG)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `article` WHERE `uploaded_by` = -1"
            cursor.execute(sql)
            articles = cursor.fetchall()
            return jsonify(articles), 200
    except pymysql.MySQLError as e:
        return jsonify({"message": "数据库错误", "错误": str(e)}), 500
    finally:
        connection.close()

@app.route('/api/search_article', methods=['GET'])
def search_article():
    keyword = request.args.get('searchContent')
    user_id = request.args.get('user_id')

    connection = pymysql.connect(**DATABASE_CONFIG)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `article` WHERE (`title` LIKE %s OR `content` LIKE %s) AND `uploaded_by`=-1"
            cursor.execute(sql, (f"%{keyword}%", f"%{keyword}%"))
            articles = cursor.fetchall()

            sql_user = "SELECT * FROM `article` WHERE (`title` LIKE %s OR `content` LIKE %s) AND `uploaded_by` =%s"
            cursor.execute(sql_user, (f"%{keyword}%", f"%{keyword}%",user_id))
            articles_user = cursor.fetchall()
            return jsonify({'filtered_articles':articles,'filterd_articles_user':articles_user}), 200
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
