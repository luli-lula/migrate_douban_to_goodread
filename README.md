# 豆瓣读书迁移到Goodread

这个工具可以帮助你导出豆瓣读书的数据，并转换为适合导入 Goodreads 的格式。
主要都是参考这位repo：[douban_read_download](https://github.com/geekplux/douban_read_download)
安装过程我自己出现了python版本问题，用Cursor的建议修改了一部分，为了减少账号被封风险，增价了延时（可以自己修改）。

## 功能特点

- 导出你的豆瓣读书清单
- 自动获取书籍的 ISBN 号
- 转换为 Goodreads 支持的导入格式
- 保留评分、阅读日期、笔记等信息

## Quick Start


### 1 安装依赖包

(optional) 创建虚拟python环境

```bash
python -m venv douban_read_download
```

安装依赖包

```bash
pip install -r requirements.txt
```

### 2 获取Cookie配置环境文件

1. 登录豆瓣网站
2. 打开浏览器开发者工具（F12）
3. 在 Network 标签页中找到任意请求
4. 复制完整的 Cookie 值
5. 将 Cookie 值粘贴到 `.env.example` 文件中，去掉 `.example` 后缀

Copy your cookie from douban *https://book.douban.com/mine?status=collect* page into `.env.example` file, drop the suffix `.example` then.

![](screenshot/cookie.png)

> (optional) 测试Cookie是否有效，如果有效会提示Cookie 验证成功！

```bash
python test_cookie.py
```

### 3 导出豆瓣读书数据

```bash
scrapy runspider start.py
```

Would create a CSV file named `books.csv` with all your reading records

![](screenshot/books.png)

### 4 添加ISBN信息（Goodread导入必须字段）

```bash
python add_ISBN_for_goodreads_import.py
```


完成后会生成 `goodreads_books.csv` 文件

### 5 导入Goodreads

直接在Goodreads网站，使用Import导入 `goodreads_books.csv` 文件即可

## 注意事项

- Cookie 有效期有限，如果遇到 403 错误需要更新 Cookie
- 建议适当调整抓取延迟，避免被封 IP
- 请勿将包含个人信息的 .env 文件上传到公共仓库

## 文件说明

- `start.py`: 主爬虫程序
- `add_ISBN_for_goodreads_import.py`: ISBN 获取程序
- `test_cookie.py`: Cookie 测试程序
- `requirements.txt`: 依赖包列表
- `.env`: 配置文件



