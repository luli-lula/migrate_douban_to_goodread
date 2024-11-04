import requests
from environs import Env

def test_cookie():
    # 读取环境变量
    env = Env()
    env.read_env()
    cookies_str = env("COOKIES")
    
    # 将 cookies 字符串转换为字典
    cookies = {}
    for item in cookies_str.split(';'):
        if '=' in item:
            key, value = item.strip().split('=', 1)
            cookies[key] = value
    
    # 设置请求头
    headers = {
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
    
    try:
        # 发送请求
        url = 'https://book.douban.com/mine?status=collect'
        response = requests.get(url, headers=headers, cookies=cookies)
        
        # 打印状态码和响应内容
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("Cookie 验证成功！")
            # 检查是否包含预期的内容
            if "我读过的书" in response.text:
                print("成功访问到'我读过的书'页面")
            else:
                print("警告：页面内容可能不正确")
        else:
            print(f"Cookie 验证失败！状态码：{response.status_code}")
            print("响应内容：", response.text[:200])  # 只打印前200个字符
            
    except Exception as e:
        print(f"发生错误：{str(e)}")

if __name__ == "__main__":
    test_cookie()
