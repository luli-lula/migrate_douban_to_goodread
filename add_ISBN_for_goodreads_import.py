import pandas as pd
import requests
import re
import time
from environs import Env

# 读取环境变量中的 cookies
env = Env()
env.read_env()
cookies_str = env("COOKIES")

# 将 cookies 字符串转换为字典
def convert_cookies_to_dict(cookies_str):
    cookies = {}
    for item in cookies_str.split(';'):
        if '=' in item:
            key, value = item.strip().split('=', 1)
            cookies[key] = value
    return cookies

# 读取 CSV 文件
books = pd.read_csv('./books.csv')
books = books.rename(columns={
    'title': 'Title',
    'rating': 'My Rating',
    'pub': 'Publisher',
    'read_date': 'Date Read',
    'comment': 'My Review',
})

books_urls = books['url'].tolist()

# 更完整的请求头
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Referer': 'https://book.douban.com/',
}

cookies = convert_cookies_to_dict(cookies_str)

for i, url in enumerate(books_urls):
    try:
        print(f'[{i+1}/{len(books_urls)}]', "Scraping: ", url)
        
        # 添加延迟，避免被封
        time.sleep(3)
        
        r = requests.get(url, headers=headers, cookies=cookies)
        
        if r.status_code == 200:
            matched = re.search(r'<meta property="book:isbn" content="(\d+)" />', r.text)
            isbn = matched.group(1).strip() if matched else ''
            print("ISBN: ", isbn)
            books.loc[books['url'] == url, 'ISBN'] = isbn
        else:
            print(f"Error: Status code {r.status_code} for {url}")
            
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        continue

# 保存结果
books.to_csv('./goodreads_books.csv', index=False)
print("完成！结果已保存到 goodreads_books.csv")
