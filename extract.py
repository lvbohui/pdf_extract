#!/usr/bin/env python
# data:2019/7/18
# author:xiao jiu

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from PyPDF2 import PdfFileReader, PdfFileWriter
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import nltk
import string
import time
import os


class ExtractTxt:
    def __init__(self):
        pass

    def cut_pages(self, cut_filename, start_page=1, end_page=None):
        '''
        :param filename: 要处理的pdf文件名，格式为："filename.pdf"
        :param start_page: 截取的开始页：不大于pdf总页数的整数
        :param end_page: 截取的截止页：不大于pdf总页数，不小于start_page的整数
        :return: 返回截取后的pdf文件名，格式为："output_filename.pdf"
        '''
        if end_page is None:
            reader = PdfFileReader(cut_filename)
            end_page = reader.getNumPages()

        fp = PdfFileReader(open(filename,'rb'))
        output = PdfFileWriter()
        for i in range(start_page-1, end_page):
            output.addPage(fp.getPage(i))
        output_filename = "output.pdf"
        output_stream = open(output_filename, "wb")
        output.write(output_stream)
        return output_filename

    def parse(self, fn, start_page=1, end_page=None):
        '''
        :param fn: 要处理的pdf文件名，格式为："filename.pdf"
        :param start_page: 截取的开始页：不大于pdf总页数的整数
        :param end_page: 截取的截止页：不大于pdf总页数，不小于start_page的整数
        :return: 以txt格式文件返回抽取出的文本内容，方便下一步处理,格式为："filename_extracted.txt"
        '''

        cut_file_name = ExtractTxt.cut_pages(self, fn, start_page, end_page)  # 要截取的页数，起始页到结束页
        print("截取完成，正在抽取文本...")
        # 抽取截取过的pdf文件的文本内容
        fn = open(cut_file_name, 'rb')
        parser = PDFParser(fn)  # 创建pdf文档分析器
        pdfdoc = PDFDocument()     # 创建pdf文档对象
        # 连接分析器和文档
        parser.set_document(pdfdoc)
        pdfdoc.set_parser(parser)
        # 初始化文档
        pdfdoc.initialize("")
        out_extract_name = "" .join(filename.split(".")[:-1]) + '_' + 'extracted.txt'

        if not pdfdoc.is_extractable:
            raise PDFTextExtractionNotAllowed
        else:
            resource = PDFResourceManager()  # 创建pdf资源管理器
            laparams = LAParams()   # 创建pdf参数分析器
            device = PDFPageAggregator(resource, laparams=laparams)  # 创建聚合器
            interpreter = PDFPageInterpreter(resource, device)  # 创建pdf页面对象解释器

            for page in pdfdoc.get_pages():
                # 使用界面解释器读取内容
                interpreter.process_page(page)
                # 使用聚合器获取内容
                layout = device.get_result()
                for out in layout:
                    if hasattr(out, "get_text"):
                        with open(out_extract_name, 'a', encoding="utf-8") as f:
                            # 写入方式为连续写入，因此对同一文件重复操作时需要删除上一次产生的文件
                            f.write(out.get_text())
        fn.close()
        print("抽取完成！")
        os.remove(cut_file_name)  # 删除中间文件

        return out_extract_name

    def txt_clearn(self, filename):  # 对抽取出的文本进行基本的清洗
        '''
        :param filename: 要清洗的文件名
        :param out_file_name: 清洗完成后输出的文件名
        :return: 根据需要可以返回清洗后的：字符串、列表、文本文件
        '''
        fn = open(filename, "r", encoding="utf-8")

        print("开始整理数据...")
        contest = fn.read().lower()  # 设置为小写
        # 去除标点符号
        for c in string.punctuation:
            contest = contest.replace(c, " ")

        wordList = nltk.word_tokenize(contest)

        filtered = [w for w in wordList if w not in stopwords.words("english")]  # 去除停顿符

        ps = PorterStemmer()
        filtered = [ps.stem(w) for w in filtered]

        wl = WordNetLemmatizer()
        filtered = [wl.lemmatize(w) for w in filtered]
        out_cleaned_name = "".join(filename.split(".")[:-1]) + '_' + 'cleaned.txt'

        writer = open(out_cleaned_name, 'w', encoding="utf-8")
        writer.write(" ".join(filtered))
        fn.close()
        writer.close()
        print("整理完成！")
        # return filtered   # 返回列表
        # return " ".join(filtered) # 返回字符串
        return out_cleaned_name    # 返回文件名


if __name__ == '__main__':
    filename = "3637.pdf"   # 要抽取的文件名
    time1 = time.time()

    extract = ExtractTxt()

    extracted_file_name = extract.parse(filename)   # 返回产生的txt文件名，便于下一步处理
    cleaned_file_name = extract.txt_clearn(extracted_file_name)  # 对抽取出的文件进行清洗

    time2 = time.time()
    print("总时间:%fs" % (time2 - time1))
