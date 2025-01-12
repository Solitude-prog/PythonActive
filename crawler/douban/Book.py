"""
@Author：失去了才知道珍惜
@Time：2024-12-06 0006 12:59
@FileName: Book.py
@Description：todo: 封装书籍信息
"""


# 图书类，封装图书信息
class Book:
    def __init__(self, isbn, bookType, category, bookName, bookUrl, pageUrl, author, publisher, press, original_title,
                 translator,
                 publish_year, page_count, price, binding, series, rating, rating_count, FiveStart, FourStart,
                 ThreeStart, TwoStart, OneStart, Introduction, AuthorAbout, OriginalExcerpt, PopularShortReviews):
        self.isbn = isbn
        self.bookType = bookType
        self.category = category
        self.bookName = bookName
        self.bookUrl = bookUrl
        self.pageUrl = pageUrl
        self.author = author
        self.publisher = publisher
        self.press = press
        self.original_title = original_title
        self.translator = translator
        self.publish_year = publish_year
        self.page_count = page_count
        self.price = price
        self.binding = binding
        self.series = series
        self.rating = rating
        self.rating_count = rating_count
        self.FiveStart = FiveStart
        self.FourStart = FourStart
        self.ThreeStart = ThreeStart
        self.TwoStart = TwoStart
        self.OneStart = OneStart
        self.Introduction = Introduction
        self.AuthorAbout = AuthorAbout
        self.OriginalExcerpt = OriginalExcerpt
        self.PopularShortReviews = PopularShortReviews

    def __str__(self):
        return (f"书名: {self.bookName}\n"
                f"ISBN: {self.isbn}\n"
                f"类型: {self.bookType}\n"
                f"一级分类: {self.category}\n"
                f"作者: {self.author}\n"
                f"网址: {self.bookUrl}\n"
                f"页面网址: {self.pageUrl}\n"
                f"出版社: {self.publisher}\n"
                f"出品方: {self.press}\n"
                f"原作名: {self.original_title}\n"
                f"译者: {self.translator}\n"
                f"出版年: {self.publish_year}\n"
                f"页数: {self.page_count}\n"
                f"价格: {self.price}\n"
                f"装帧: {self.binding}\n"
                f"丛书: {self.series}\n"
                f"评分: {self.rating} \n"
                f"评价人数: {self.rating_count}\n"
                f"五星好评：{self.FiveStart} \n"
                f"四星好评：{self.FourStart} \n"
                f"三星好评：{self.ThreeStart} \n"
                f"两星好评：{self.TwoStart} \n"
                f"一星好评：{self.OneStart} \n"
                f"内容简介：{self.Introduction} \n"
                f"作者简介：{self.AuthorAbout} \n"
                f"原文摘录：{self.OriginalExcerpt} \n"
                f"热门短评：{self.PopularShortReviews} \n"
                )

    def to_dict(self):
        return {
            "isbn": self.isbn,
            "bookName": self.bookName,
            "bookType": self.bookType,
            "category": self.category,
            "author": self.author,
            "bookUrl": self.bookUrl,
            "pageUrl": self.pageUrl,
            "publisher": self.publisher,
            "press": self.press,
            "original_title": self.original_title,
            "translator": self.translator,
            "publish_year": self.publish_year,
            "page_count": self.page_count,
            "price": self.price,
            "binding": self.binding,
            "series": self.series,
            "rating": self.rating,
            "rating_count": self.rating_count,
            "FiveStart": self.FiveStart,
            "FourStart": self.FourStart,
            "ThreeStart": self.ThreeStart,
            "TwoStart": self.TwoStart,
            "OneStart": self.OneStart,
            "Introduction": self.Introduction,
            "AuthorAbout": self.AuthorAbout,
            "OriginalExcerpt": self.OriginalExcerpt,
            "PopularShortReviews": self.PopularShortReviews
        }
