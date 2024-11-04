import scrapy
import pandas as pd
from environs import Env
import json

env = Env()
env.read_env()
cookies_str = env("COOKIES")

# 辅助函数
def _s(s):
    return ''.join(s) if s else ''

# 将 cookies 字符串转换为字典
def convert_cookies_to_dict(cookies_str):
    cookies = {}
    for item in cookies_str.split(';'):
        if '=' in item:
            key, value = item.strip().split('=', 1)
            cookies[key] = value
    return cookies

class DoubanSpider(scrapy.Spider):
    name = 'douban_spider'
    start_url = 'https://book.douban.com/mine?status=collect'
    
    custom_settings = {
        'DOWNLOAD_DELAY': 3,  # 增加延迟
        'COOKIES_ENABLED': True,
        'ROBOTSTXT_OBEY': False,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Referer': 'https://book.douban.com/',
            'Host': 'book.douban.com',
            'Sec-Ch-Ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }
    }

    df = pd.DataFrame(columns=['title', 'url', 'pub',
                               'rating', 'read_date', 'tags', 'comment'])

    def start_requests(self):
        cookies = convert_cookies_to_dict(cookies_str)
        yield scrapy.Request(
            url=self.start_url,
            cookies=cookies,
            callback=self.parse_list,
            dont_filter=True
        )

    def parse_list(self, response):
        print('Read book list: ', response.url)
        book_list = response.css('#content div.article ul li.subject-item')
        for item in book_list:
            title = item.css('div.info > h2 > a::text').get().strip()
            print('Is scraping: ', title)
            try:
                rating = _s(item.css(
                    'div.info div.short-note > div:nth-child(1) > span:nth-child(1)::attr(class)').get()).strip()
                rating = int(_s(filter(str.isdigit, rating))
                             ) if rating.startswith('rating') else ''
                book = {
                    'title': title,
                    'url': _s(item.css('div.info > h2 > a::attr(href)').get()),
                    'pub': _s(item.css('div.info > div.pub::text').get()).strip(),
                    'rating': rating,
                    'read_date': _s(item.css('div.info div.short-note > div:nth-child(1) > span.date::text').get()).replace('读过', '').strip(),
                    'tags': _s(item.css('div.info div.short-note > div:nth-child(1) > span.tags::text').get()).replace('标签:', '').strip(),
                    'comment': _s(item.css('div.info div.short-note > p.comment::text').get()).strip(),
                }
                self.df = pd.concat([self.df, pd.DataFrame([book])], ignore_index=True)
            except Exception as error:
                print('error on: ', title, error)

        next_page = response.css(
            '#content div.article div.paginator > span.next > a::attr(href)').get()
        if next_page:
            url = response.urljoin(next_page)
            print("next page: ", url)
            # 使用 custom_settings 中的 DEFAULT_REQUEST_HEADERS
            yield scrapy.Request(
                url, 
                callback=self.parse_list, 
                headers=self.custom_settings['DEFAULT_REQUEST_HEADERS']
            )
        else:
            self.df.to_csv('./books.csv')
