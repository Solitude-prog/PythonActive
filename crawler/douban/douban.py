"""
@Author：失去了才知道珍惜
@Time：2024-12-04 0004 23:51
@FileName: douban.py
@Description：todo: 
"""
from datetime import datetime
import time
from doubanBookType import *
from Utiles import *
from Book import Book


# 获取图书页面内容
def get_book_info(url):
    response = requests.get(url, headers=getHeader())

    if response.status_code != 200:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "无法访问该页面", url)
        return None, None

    # 使用 lxml 解析页面
    tree = html.fromstring(response.text)

    # 提取//*[@id="info"]下的所有内容
    info_section = tree.xpath('//*[@id="info"]')[0]  # 获取整个info

    # 获取纯文本信息，字符串类型
    raw_text = info_section.text_content()

    # 清理洗文本内容：去除多余的空行、空格等干扰信息
    cleaned_text = re.sub(r'\s+', ' ', raw_text)  # 将多个空白字符替换为一个空格
    cleaned_text = cleaned_text.strip()  # 去除首尾空白字符
    # 判断空
    cleaned_text = default_info() if check_empty(cleaned_text) else cleaned_text
    bookName = tree.xpath('//*[@id="wrapper"]/h1/span/text()')[0]  # 书名

    rating = safe_get('//*[@id="interest_sectl"]/div/div[2]/strong/text()', tree)  # 豆瓣评分
    rating_count = safe_get('//*[@id="interest_sectl"]/div/div[2]/div/div[2]/span/a/span/text()', tree)  # 评价人数
    FiveStart = safe_get('//*[@id="interest_sectl"]/div/span[2]/text()', tree)  # 五星
    FourStart = safe_get('//*[@id="interest_sectl"]/div/span[4]/text()', tree)  # 四星
    ThreeStart = safe_get('//*[@id="interest_sectl"]/div/span[6]/text()', tree)  # 三星
    TwoStart = safe_get('//*[@id="interest_sectl"]/div/span[8]/text()', tree)  # 两星
    OneStart = safe_get('//*[@id="interest_sectl"]/div/span[10]/text()', tree)  # 一星

    # 使用XPath或者CSS选择器选择指定的div
    Introduction = safe_other('//*[@id="link-report"]/span[2]/div/div//p//text()', tree)
    # 提取div内所有p标签的文本，并将它们拼接成一行

    AuthorAbout = safe_other('//*[@id="content"]/div/div[1]/div[3]/div[3]/span[1]/div//p//text()', tree)

    OriginalExcerpt = safe_other('//*[@id="content"]/div/div[1]/div[3]/div[7]/div/ul/li[1]/figure/text()[1]', tree)[:-1]

    PopularShortReviews = safe_other('//*[@id="score"]/ul/li[1]/div/p/span//text()', tree)[:-1]

    dict = {"OneStart": OneStart, "TwoStart": TwoStart, "ThreeStart": ThreeStart, "FourStart": FourStart,
            "FiveStart": FiveStart, "rating": rating, "rating_count": rating_count, "bookName": bookName,
            "bookUrl": url,
            "Introduction": Introduction, "AuthorAbout": AuthorAbout, "OriginalExcerpt": OriginalExcerpt,
            "PopularShortReviews": PopularShortReviews}
    # print(FiveStart, FourStart, ThreeStart, TwoStart, OneStart)
    return cleaned_text, dict


# 用对象封装数据
def assemble(text, dict, bookType, pageUrl, category):
    book_info = parse_book_info(text)
    # 创建 Book 对象，进行数据封装
    book = Book(
        isbn=book_info["isbn"],
        bookName=dict["bookName"],
        bookType=bookType,
        category=category,
        author=book_info["author"],
        bookUrl=dict["bookUrl"],
        pageUrl=pageUrl,
        publisher=book_info["publisher"],
        press=book_info["press"],
        original_title=book_info["original_title"],
        translator=book_info["translator"],
        publish_year=book_info["publish_year"],
        page_count=book_info["page_count"],
        price=book_info["price"],
        binding=book_info["binding"],
        series=book_info["series"],
        rating=dict["rating"],
        rating_count=dict["rating_count"],
        FiveStart=dict["FiveStart"],
        FourStart=dict["FourStart"],
        ThreeStart=dict["ThreeStart"],
        TwoStart=dict["TwoStart"],
        OneStart=dict["OneStart"],
        Introduction=dict["Introduction"],
        AuthorAbout=dict["AuthorAbout"],
        OriginalExcerpt=dict["OriginalExcerpt"],
        PopularShortReviews=dict["PopularShortReviews"]
    )
    return book


# 获取每一页的图书URL
def get_book_urls(book_type, page_number):
    data = {}
    pages_url = f'https://book.douban.com/tag/{book_type}?start={page_number * 20}&type=T'
    # 请求页面内容
    response = requests.get(pages_url, headers=getHeader())
    if response.status_code != 200:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), f"无法访问页面: {pages_url}")

        return None, 0

    # 使用 lxml 解析页面
    tree = html.fromstring(response.text)

    # 提供的 XPath 路径提取每本书的 URL
    book_urls = tree.xpath('//*[@id="subject_list"]/ul/li/div[2]/h2/a/@href')
    data[pages_url] = book_urls

    count = len(book_urls)
    result = clean_empty(data)
    return result, count  # {页url:[url]}


# 获取所有图书URL
def get_all_book_urls(book_type, pages):
    all_book_urls = {}
    count = 0
    # print(f"正在爬取{book_type} 第 {pages}页的所有图书url...")
    for page in range(pages):
        time.sleep(random.uniform(1, 3))  # 豆瓣有反爬机制，频繁访问会被关小黑屋
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "-----------",
              f"正在采集{book_type} - 第 {page + 1} 页的所有图书url .....")

        book_pages_url, url_count = get_book_urls(book_type, page)
        if book_pages_url is None: continue
        book_pages_url = clean_empty(book_pages_url)

        all_book_urls.update(book_pages_url)

        count += url_count

    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "-----------", f"{book_type}的所有图书url  采集完成")
    result = clean_empty(all_book_urls)
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "-----------", f"{book_type} 类型 一共采集到 {count} 条url")
    return result, count  # {页url:[url]}


def getAllBookInfo(bookTypes, pages):
    allBook = []  # 定义空列表进行接收
    all_count = 0
    category_count = 0
    type_count = 0
    for (category, types) in bookTypes.items():
        time.sleep(random.uniform(2, 7))  # 豆瓣有反爬机制，频繁访问会被关小黑屋
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "-----------", f"开始采集{category}中的图书")
        if check_empty(types): continue

        category_count += 1
        for type in types:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "-----------",
                  f"开始采集{category} - {type}的所有书籍url")
            book_urls, urls_count = get_all_book_urls(type, pages)

            if check_empty(book_urls): continue
            type_count += 1
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "-----------",
                  f"开始采集{category} - {type}的所有书籍信息")
            for (page_url, urls) in book_urls.items():

                if check_empty(urls): continue

                for url in urls:
                    time.sleep(random.uniform(2, 5))  # 豆瓣有反爬机制，频繁访问会被关小黑屋
                    clean_txt, dict = get_book_info(url)

                    if clean_txt is None: continue  # 这个很关键
                    if check_empty(clean_txt): continue

                    book = assemble(clean_txt, dict, type, page_url, category)
                    if book.bookName != 404 or book.isbn != 888888:
                        allBook.append(book)
                        # print(book)
                        all_count += 1
                        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "-----------",
                              f"{category} - {type} - 《{book.bookName}》 已采集完成：", url)

            write(allBook, "data", category, type)
            allBook.clear()

    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "-----------", "本次采集一级分类数量为：", category_count)
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "-----------", "本次采集二级分类数量为：", type_count)
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "-----------", "本次采集总数量为：", all_count)
    # return allBook


if __name__ == '__main__':
    start = time.time()
    # ['文学'], ['小说'],,'互联网','科学'
    bookTypes = select_new(types=['小说'])
    pages = 50  # 最大为50，50页以后没有了
    books = getAllBookInfo(bookTypes, pages)
    # df = BookToDataFrame(books)
    # df.to_csv("./Books.csv", encoding="utf8", index=False)

    level_count(bookTypes)

    duration = ((time.time() - start) / 3600)
    print("代码运行结束，总耗时长为", '%.3f' % duration, "小时")
