import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import pymysql
import pymysql.cursors
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'db': 'foreign_magazine_data',
    'cursorclass': pymysql.cursors.DictCursor
}


def fetch_article_info(target_url):
    headers = {'Accept-Charset': 'utf-8'}
    response = requests.get(target_url, headers=headers)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')
    # 获取标题
    title_td = soup.find('td', id='TRS_Editor_title')
    if title_td:
        title = title_td.text  
    else:
        return "No td tag with id 'article_title' found."
    
    # 获取上传时间和来源
    art_info_td = soup.find('td', class_='ly4')
    if art_info_td:
        art_info = art_info_td.text
        update_time = re.search(r'\d{4}-\d{2}-\d{2}',art_info).group()
        source = re.search(r'Source:(.*)',art_info).group(1)
    
    # 获取文章内容
    art_content_div = soup.find('div', class_='TRS_Editor')
    additional_css = """
            .TRS_Editor {
                text-align: justify;
                text-justify: inter-word;
            }

            .TRS_Editor P, .TRS_Editor DIV, .TRS_Editor TD, .TRS_Editor TH, .TRS_Editor SPAN, .TRS_Editor FONT, .TRS_Editor UL, .TRS_Editor LI, .TRS_Editor A {
                margin-top: 15px;
                margin-bottom: 15px;
                line-height: 1.4;
            }
            """

    if art_content_div:
        # 添加或追加样式
        style_tag = art_content_div.find('style')
        if style_tag:
            style_tag.string += additional_css  
        else:
            # 如果没有找到 style 标签，创建一个新的并添加到 art_content_div
            new_style_tag = soup.new_tag('style')
            new_style_tag.string = additional_css
            art_content_div.insert(0, new_style_tag)
        
        # art_text 用于存储文章的纯文本内容
        art_text = ''
        p_tags = art_content_div.find_all('p')
        for p in p_tags:
            # 遍历所有的 <p> 标签，删除特定的 style 设置；
            if 'style' in p.attrs:
                if (p['style']=='text-align: left;'):
                    del p['style']
            
            if re.search('[a-zA-Z]', p.text):
                art_text += p.text + '\n'


        # 更新图片路径
        images = art_content_div.find_all('img')
        for img in images:
            if img.has_attr('src'):
                absolute_url = urljoin(target_url, img['src'])
                img['src'] = absolute_url  

        # 更新 content 为修改后的 art_content_div
        content = art_content_div

    # 获取文章分类
    catogory_div = soup.find('a', class_='lm-2016e CurrChnlCls')
    catogory = catogory_div.text

    
    connection = pymysql.connect(**DATABASE_CONFIG)
    try:
        with connection.cursor() as cursor:
            check_exist_sql = "SELECT * FROM `article` WHERE `title` = %s"
            art_exist = cursor.execute(check_exist_sql, (title,))
            if not art_exist:
                sql = "INSERT INTO `article` (`title`, `content`, `article_source`, `update_time`, `category`,`art_text`) VALUES (%s, %s, %s, %s, %s,%s)"
                cursor.execute(sql, (title, content, source, update_time, catogory,art_text))
                connection.commit()
                print(f"数据插入成功；{title}")
            else:
                print("文章暂时未更新")
    except pymysql.MySQLError as e:
        print(f"数据插入失败；{e}")
    finally:
        connection.close()




def fetch_url(target_site):
    response = requests.get(target_site)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 查找第一个class='bian8'的div标签
    div_tag = soup.find('div', class_='bian8')
    
    # 在找到的div标签中查找第一个a标签
    if div_tag:
        a_tag = div_tag.find('a')
        # 如果a标签存在，获取其href属性
        if a_tag:
            rel_url = a_tag.get('href')  # 返回链接
            abs_url = urljoin(target_site, rel_url)
            return abs_url
        else:
            return "在该div中没有找到a标签。"
    else:
        return "没有属性值为'bian8'的div标签。"

# 指定要抓取的网站
target_sites = ['https://www.bjreview.com/Lifestyle/','https://www.bjreview.com/China/','https://www.bjreview.com/World/','https://www.bjreview.com/Business/']
for target_site in target_sites:
    target_url = fetch_url(target_site)
    fetch_article_info(target_url)
