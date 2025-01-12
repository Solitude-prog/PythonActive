"""
@FileName: doubanBookType.py
@Description：todo: 
"""

import copy
import json
from lxml import html
from Utiles import *

url = "https://book.douban.com/tag/?view=type&icn=index-sorttags-hot"

all = {
    '文学': ['小说', '文学', '外国文学', '经典', '中国文学', '随笔', '日本文学', '散文', '村上春树', '诗歌', '童话',
             '名著', '儿童文学', '古典文学', '余华', '王小波', '当代文学', '杂文', '张爱玲', '外国名著', '鲁迅',
             '钱钟书', '诗词', '茨威格', '米兰·昆德拉', '杜拉斯', '港台'],
    '流行': ['漫画', '推理', '绘本', '悬疑', '科幻', '东野圭吾', '青春', '言情', '推理小说', '奇幻', '日本漫画',
             '武侠', '耽美', '科幻小说', '网络小说', '三毛', '韩寒', '亦舒', '阿加莎·克里斯蒂', '金庸', '穿越',
             '安妮宝贝', '轻小说', '魔幻', '郭敬明', '青春文学', '几米', 'J.K.罗琳', '幾米', '校园', '张小娴',
             '古龙', '高木直子', '沧月', '余秋雨', '王朔'],
    '文化': ['历史', '心理学', '哲学', '社会学', '传记', '文化', '艺术', '社会', '政治', '设计', '政治学', '宗教',
             '电影', '建筑', '中国历史', '数学', '回忆录', '思想', '人物传记', '艺术史', '国学', '人文', '音乐',
             '绘画', '戏剧', '西方哲学', '近代史', '二战', '军事', '佛教', '考古', '自由主义', '美术'],
    '生活': ['爱情', '成长', '生活', '心理', '女性', '旅行', '励志', '教育', '摄影', '职场', '美食', '游记', '健康',
             '灵修', '情感', '人际关系', '两性', '养生', '手工', '家居', '自助游'],
    '经管': ['经济学', '管理', '经济', '商业', '金融', '投资', '营销', '理财', '创业', '股票', '广告', '企业史',
             '策划'],
    '科技': ['科普', '互联网', '科学', '编程', '交互设计', '算法', '用户体验', '科技', 'web', '交互', '通信', 'UE',
             '神经网络', 'UCD', '程序']}


def category_one(url):
    response = requests.get(url, headers=getHeader())

    if response.status_code != 200:
        print("无法访问该页面")
        return None

    # 使用 lxml 解析页面
    tree = html.fromstring(response.text)

    h2_texts = tree.xpath('//*[@id="content"]//h2/text()')
    # 清洗文本：去除多余空白和特殊字符，只保留中文部分
    cleaned_text = [
        re.sub(r'\s+|·+', '', text.strip())
        for text in h2_texts if text.strip() and not re.match(r'^[·\s]+$', text.strip())
    ]

    return cleaned_text, tree


def category_two(url: str):
    cate, tree = category_one(url)
    allData = {}
    # 文学
    # 使用XPath获取指定位置的所有a标签中的文本
    literature = tree.xpath('//*[@id="content"]/div/div[1]/div[2]/div[1]/table/tbody//a/text()')
    allData[cate[0]] = literature

    # 流行：popular
    popular = tree.xpath('//*[@id="content"]/div/div[1]/div[2]/div[2]/table/tbody//a/text()')
    allData[cate[1]] = popular

    # 文化
    culture = tree.xpath('//*[@id="content"]/div/div[1]/div[2]/div[3]/table/tbody//a/text()')
    allData[cate[2]] = culture

    #     life生活
    life = tree.xpath('//*[@id="content"]/div/div[1]/div[2]/div[4]/table/tbody//a/text()')
    allData[cate[3]] = life

    # Management 经管
    Management = tree.xpath('//*[@id="content"]/div/div[1]/div[2]/div[5]/table/tbody//a/text()')
    allData[cate[4]] = Management

    # 科学
    technology = tree.xpath('//*[@id="content"]/div/div[1]/div[2]/div[6]/table/tbody//a/text()')
    allData[cate[5]] = technology

    # print(allData)
    # print(type(allData))

    return allData

# 情况一：所有一级分类、二级分类都要
# 情况二：要一级分类下的所有
# 情况三：只要某些二级分类
# 情况四：一级分类没用指定二级分类则返回对应一级分类的所有子类
# 情况五：二级分类不在指定的一级分类中

# 函数返回的是：{一级分类：[一个或多个二级分类]}
# 字典中重复的key会被后面添加的key覆盖
def select_new(OneLevels=None, types=None, reset=False):
    global all
    data = {}
    # 拿到所有的一级分类，二级分类

    if reset:
        all = category_two(url)

    # 不传递参数默认返回所有数据
    if OneLevels is None and types is None:
        return all

    for (key, list) in all.items():  # key是一级分类，value是二级分类列表
        if OneLevels is not None and types is None:  # 一级分类不为空，但是二级分类为空，返回的是指定一级分类下的所有二级分类
            for oneleve in OneLevels:
                if oneleve == key:
                    data[key] = list
        elif OneLevels is None and types is not None:  # 一级分类为空，但二级分类不为空，返回的是指定的二级分类以及其所属的一级分类
            lit = []  # 用于接收同一个一级分类的二级分类
            for type in types:  # 遍历指定的二级分类
                for i in list:  # 遍历二级分类
                    if type == i:  # 如果二级分类在此
                        lit.append(i)  # 加入临时列表
            data[key] = lit  # 遍历完了后添加到字典中
        elif OneLevels is not None and types is not None:
            # 最后这中情况是以上两种情况的结合体，既指定的一级分类，也指定了二级分类，
            # 指定的二级分类所属的一级分类可能不在指定的一级分类中，返回 {不在指定的一级分类中的一级分类：[指定的二级分类1，指定的二级分类二····]}
            # 指定的一级分类下的二级分类可能不在指定的二级分类中，  返回 {指定的一级分类：[所属一级分类的所有二级分类]}
            # 最终返回的结果 {
            #              指定的一级分类：[所属一级分类的所有二级分类],
            #             不在指定的一级分类中的一级分类：[指定的二级分类1，指定的二级分类二····]
            #              }
            for onelevel in OneLevels:  # 将指定的一级分类及其二级分类添加到字典中
                if onelevel == key:
                    data[key] = list

            tmp_list = []  # 用于接收同一个一级分类的二级分类
            for type in types:  # 遍历指定二级分类
                for i in list:  # 遍历二级分类
                    if i == type:  # 如果是指定的二级分类就将这个二级分类添加到列表中
                        tmp_list.append(i)

            # 遍历到其他类型时会将空列表也添加到字典中
            # 如果不做清洗会将结果字典中的第一种情况给破坏掉
            # 原因是：在做一级分类处理时是将指定的一级分类及其二级分类添加到字典中，
            # 如果在处理二级分类时指定的二级分类又不在指定的一级分类中就会将对应的一级分类中的二级分类覆盖(空的)
            if len(tmp_list) != 0:
                data[key] = tmp_list

    # 最后做一次清洗，将空列表剔除，保证返回的是有效列表
    result = clean_empty(data)

    return result


def Counter_selection(remove_level: list = None, remove_type: list = None,reset:bool=False):
    data = {}
    global all

    if reset:
        all=category_two(url)

    if remove_level is None and remove_type is None:
        data.update(all)

    for (category, type_list) in all.items():
        if remove_level is not None and remove_type is None:
            for level in remove_level:
                if level != category:
                    data[category] = type_list
        elif remove_level is None and remove_type is not None:
            tmp_list = []
            for ty in remove_type:
                for ty_l in type_list:
                    if ty != ty_l:
                        tmp_list.append(ty_l)
            data[category] = tmp_list
        elif remove_level is not None and remove_type is not None:
            for level in remove_level:
                if level != category:
                    data[category] = type_list

            tmp_list = []
            for ty in remove_type:
                for ty_l in type_list:
                    if ty != ty_l:
                        tmp_list.append(ty_l)
            if len(tmp_list) != 0:
                data[category] = tmp_list


    result = check_empty(data)
    return result



def check_dict(dict1: dict, dict2: dict):
    # 对字典中的列表排序后比较
    sorted_dict1 = {k: sorted(v) for k, v in dict1.items()}
    sorted_dict2 = {k: sorted(v) for k, v in dict2.items()}

    return sorted_dict1 == sorted_dict2


if __name__ == '__main__':
    # "文学","经典","中国文学"
    OneLevels = ["文学", "流行", "科技"]
    types = ["经典", '中国文学', '小说', '科幻', "成长"]
    remove = ['日本文学', '外国名著']

    dict = select_new(OneLevels=OneLevels, types=types)

    text = {
        '文学': ['经典', '中国文学', '小说'],
        '流行': ['科幻'],
        '科技': ['科普', '互联网', '科学', '编程', '交互设计', '算法', '用户体验', '科技', 'web', '交互', '通信', 'UE',
                 '神经网络', 'UCD', '程序'],
        '生活': ['成长']
    }
    # print(check_dict(dict,text))
    #
    print(dict)
    # print(type(dict))
    count=0
    for (k, v) in all.items():
        if k=='文化':
            for i in v:
                count+=1
    print(count)
