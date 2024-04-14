import requests
from lxml import etree
import re
import pymysql
import pymysql.cursors

DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'db': 'foreign_magazine_data',
    'cursorclass': pymysql.cursors.DictCursor
}

URLS = []

def fetch_article_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功

        # 解析 HTML
        tree = etree.HTML(response.content)

        title = tree.xpath('//h1')[0].text

        content_div = tree.xpath('//div[@id="Content"]')[0]
        content = etree.tostring(content_div, pretty_print=True, encoding='unicode')

        bread_nav = tree.xpath('//ol[@id="bread-nav1"]')[0]
        if len(bread_nav) > 0:
            catogory = bread_nav.xpath('./li/a')[1].text

        article_info = tree.xpath('//span[@class="info_l"]')[0].text
    
        info_parts = re.search(r'(.*)\|\s*Updated:(.*)', article_info)
        if info_parts:
            source = info_parts.group(1)
            date = info_parts.group(2)
        
        connection = pymysql.connect(**DATABASE_CONFIG)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `article` (`title`, `content`, `article_source`, `update_time`, `category`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (title, content, source, date, catogory))
                connection.commit()
        except pymysql.MySQLError as e:
            print(f"数据插入失败；{e}")
        finally:
            connection.close()

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

def fetch_urls(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功

        # 解析 HTML
        tree = etree.HTML(response.content)

        
        fcon_divs = tree.xpath('//div[@class="fcon"]')
        fcon_divs = fcon_divs[:-1]  # 重新赋值，不包括最后一个元素

        
        for fcon_div in fcon_divs:
            first_a_tag = fcon_div.xpath('./a')[0]
            url = 'https:' + first_a_tag.get('href')
            URLS.append(url)
        

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")


target_site = 'https://www.chinadaily.com.cn/'
fetch_urls(target_site)
for url in URLS:
    fetch_article_content(url)
