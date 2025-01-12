"""
@FileName: Utiles.py
@Description：todo: 工具函数
"""
import os
import random
import re
from pathlib import Path
import requests
# from fake_useragent import UserAgent
import pandas as pd


def getHeader():
    # 随机获取一个headers
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55',

    ]
    # ua = UserAgent()
    # for i in range(500):
    #     user_agents.append(ua.random)
    # 打开文件并读取内容
    # with open("useagents.txt", "r", encoding="utf-8") as file:
    #     content = file.read()
    # data = content.split('\n')
    # user_agents.extend(data)
    headers = {
        "Host": "book.douban.com",
        "referer": "https://www.baidu.com/",
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "close"
    }
    return headers


def safe_get(xpath, tree, default=0):
    """辅助函数，安全地获取 XPath 的值，若无值则返回默认值"""
    result = tree.xpath(xpath)
    return result[0] if result else default


def level_count(bookTypes: dict):
    one_level_count = 0
    two_level_count = 0
    for (k, v) in bookTypes.items():
        one_level_count += 1
        for i in v:
            two_level_count += 1
    print(f"本次采集一级分类数量为 {one_level_count} , 二级分类数量为：{two_level_count}")


def safe_other(xpath, tree, default=''):
    txts = tree.xpath(xpath)
    if len(txts) == 0:
        return default
    else:
        clean_txt = " ".join(re
                             .sub(r'\s+', ' ', text)  # 去除多余的空格空行
                             .strip()  # 去除左右两边
                             .replace('...', '')  # 去除省略号
                             .replace('(展开全部)', '')
                             .replace('—', '')
                             .replace('…', '')
                             # .replace('——', '')
                             .replace('-', '')
                             for text in txts)
        return clean_txt


def BookToDataFrame(allBook):
    book_dicts = [book.to_dict() for book in allBook]  # 转换成字典类型
    df = pd.DataFrame(book_dicts)
    return df


def Scheduling(filename, books, len):
    if len(books) == 0: return

    if len(books) % 200 == 0:
        df = BookToDataFrame(books)
        df.to_csv(filename, index=False, encoding="utf8")


def parse_book_info(text):
    # 利用正则表达式匹配各个字段，提取数据
    if len(text) == 0:
        book_info = {
            "author": 404,
            "publisher": 404,
            "press": 404,
            "original_title": 404,
            "translator": 404,
            "publish_year": "9999-99",
            "page_count": 404,
            "price": 123456,
            "binding": 404,
            "series": 404,
            "isbn": 888888
        }
    else:
        book_info = {
            "author": re.search(r"作者: (.*?) 出版社", text).group(1) if re.search(r"作者: (.*?) 出版社", text) else "",
            "publisher": re.search(r"出版社: (.*?) 出品方", text).group(1) if re.search(r"出版社: (.*?) 出品方",
                                                                                        text) else "",
            "press": re.search(r"出品方: (.*?) 原作名", text).group(1) if re.search(r"出品方: (.*?) 原作名",
                                                                                    text) else "",
            "original_title": re.search(r"原作名: (.*?) 译者", text).group(1) if re.search(r"原作名: (.*?) 译者",
                                                                                           text) else "",
            "translator": re.search(r"译者: (.*?) 出版年", text).group(1) if re.search(r"译者: (.*?) 出版年",
                                                                                       text) else "",
            "publish_year": re.search(r"出版年: (.*?) 页数", text).group(1) if re.search(r"出版年: (.*?) 页数",
                                                                                         text) else "",
            "page_count": re.search(r"页数: (.*?) 定价", text).group(1) if re.search(r"页数: (.*?) 定价", text) else "",
            "price": re.search(r"定价: (.*?) 装帧", text).group(1) if re.search(r"定价: (.*?) 装帧", text) else "",
            "binding": re.search(r"装帧: (.*?) 丛书", text).group(1) if re.search(r"装帧: (.*?) 丛书", text) else "",
            "series": re.search(r"丛书: (.*?) ISBN", text).group(1) if re.search(r"丛书: (.*?) ISBN", text) else "",
            "isbn": re.search(r"ISBN: (\d+)", text).group(1) if re.search(r"ISBN: (\d+)", text) else ""
        }
    return book_info


def default_info():
    book_info = ("作者: 404 "
                 "出版社: 404 "
                 "出品方: 404 "
                 "原作名: 404 "
                 "译者: 404 "
                 "出版年: 9999-99 "
                 "页数: 404 "
                 "定价: 123456 "
                 "装帧: 404 "
                 "丛书: 404 "
                 "ISBN: 123456")
    return book_info


def clean_empty(dict: dict):
    if dict is None or len(dict) == 0: return
    result = {}
    for (key, values) in dict.items():
        if len(values) != 0:
            result[key] = values
    return result


def check_empty(item):
    return False if len(item) != 0 else True


def create_folder(folder_path):
    # 如果是相对路径，转换为绝对路径
    folder_path = Path(folder_path).resolve()  # resolve() 会返回绝对路径

    # 检查文件夹是否存在，如果不存在就创建
    if not folder_path.exists():
        folder_path.mkdir(parents=True, exist_ok=True)
    #     print(f"文件夹 '{folder_path}' 已创建。")
    # else:
    #     print(f"文件夹 '{folder_path}' 已存在。")


def index_out(item):
    return True if len(item) == 0 else False


def getProxies():
    ips = ['120.42.248.162:20131', '120.42.248.213:20043', '120.42.248.185:20043', '60.188.79.115:20069',
           '60.188.79.112:20291', '60.188.79.113:20241', '120.42.248.161:20167', '120.42.248.213:20119',
           '60.188.79.103:20297', '60.188.79.116:20231', '120.42.248.188:20055', '60.188.79.103:20147',
           '60.188.79.111:20063', '60.188.79.115:20065', '27.152.28.176:20051', '120.42.248.188:20043',
           '120.42.248.194:20041', '60.188.79.112:20065', '60.188.79.110:20189', '60.188.79.117:20373',
           '60.188.79.110:20315', '60.188.79.111:20191', '120.42.248.188:20015', '60.188.79.115:20385',
           '60.188.79.112:20305', '60.188.79.115:20123', '60.188.79.114:20239', '60.188.79.112:20123',
           '60.188.79.105:20137', '60.188.79.118:20321', '60.188.79.110:20231', '27.152.28.189:20181',
           '60.188.79.115:20149', '60.188.79.114:20051', '120.42.248.185:20087', '120.42.248.185:20059',
           '60.188.79.115:20279', '60.188.79.112:20279', '60.188.79.116:20311', '60.188.79.111:20267',
           '60.188.79.110:20047', '120.42.248.213:20075', '60.188.79.114:20271', '120.42.248.193:20017',
           '120.42.248.161:20003', '27.152.28.176:20011', '60.188.79.117:20387', '120.42.248.213:20197',
           '60.188.79.113:20339', '120.42.248.201:20097', '60.188.79.115:20113', '60.188.79.113:20117',
           '27.152.28.177:20189', '60.188.79.112:20253', '120.42.248.203:20093', '120.42.248.188:20049',
           '120.42.248.215:20035', '60.188.79.110:20305', '60.188.79.113:20283', '120.42.248.169:20065',
           '60.188.79.110:20117', '120.42.248.185:20065', '120.42.248.162:20009', '60.188.79.113:20279',
           '60.188.79.103:20093', '60.188.79.111:20229', '120.42.248.213:20051', '60.188.79.113:20171',
           '60.188.79.115:20165', '60.188.79.111:20237', '60.188.79.110:20195', '60.188.79.112:20197',
           '60.188.79.112:20327', '60.188.79.112:20107', '60.188.79.113:20213', '60.188.79.105:20391',
           '60.188.79.110:20053', '60.188.79.114:20199', '60.188.79.110:20171', '60.188.79.111:20205',
           '60.188.79.112:20209', '60.188.79.110:20163', '27.152.28.177:20085', '60.188.79.112:20349',
           '60.188.79.114:20247', '60.188.79.112:20093', '60.188.79.115:20101', '120.42.248.209:20143',
           '60.188.79.116:20229', '60.188.79.115:20033', '120.42.248.188:20011', '60.188.79.110:20293',
           '120.42.248.172:20107', '120.42.248.169:20171', '60.188.79.115:20047', '120.42.248.194:20057']

    list = []
    for ip in ips:
        dict = {
            'http': f'http://{ip}',
            'https': f'https://{ip}',
        }
        list.append(dict)

    result = []

    for proxies in list:
        try:
            resp = requests.get(url="https://www.baidu.com/", proxies=proxies, headers=getHeader(), timeout=5)
            # 获取 状态码为200
            if resp.status_code == 200:
                result.append(proxies)
                print(proxies, "可用")
        except Exception as e:
            pass

    return result


def merge_csv_files(directory, toNewCSV: bool = False):
    # 存放所有 CSV 文件的路径
    csv_files = []

    # 使用 os.walk 遍历目录及其子目录
    for root, dirs, files in os.walk(directory):
        # 筛选出 CSV 文件
        for file in files:
            if file.endswith('.csv'):
                # 获取文件的完整路径
                csv_files.append(os.path.join(root, file))

    # 合并所有 CSV 文件
    dfs = []  # 存放所有 DataFrame 的列表
    for csv_file in csv_files:
        # 读取 CSV 文件并将其添加到 dfs 列表中
        df = pd.read_csv(csv_file,index_col='isbn')
        dfs.append(df)

    # 合并所有 DataFrame
    merged_df = pd.concat(dfs, ignore_index=False)

    if toNewCSV:
        merged_df.to_csv(f"{directory}/allBooks.csv")

    return merged_df

def write(books,path,category,type):
    df = BookToDataFrame(books)
    create_folder(f"{path}/{category}")
    df.to_csv(f"{path}/{category}/{type}_books.csv", index=False, encoding="utf8")
    print(f"本次 {type} 采集数量为： {len(books)} 条")

