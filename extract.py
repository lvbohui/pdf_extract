#!/usr/bin/env python
# data:2019/7/18
# author:xiao jiu

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from PyPDF2 import PdfFileReader, PdfFileWriter
import nltk
import time
import os
import re
import logging
logging.Logger.propagate = False
logging.getLogger().setLevel(logging.ERROR)


class ExtractText:
    def __init__(self, file_name, start_page=1, end_page=None):
        self.File_name = file_name
        self.Start_page = start_page
        if end_page is None:
            reader = PdfFileReader(file_name)
            self.End_page = reader.getNumPages()
        else:
            self.End_page = end_page
        pass

    def cut_pages(self):

        # :return: 返回截取后的pdf文件名，格式为："output_filename.pdf"
        if self.End_page is None:
            reader = PdfFileReader(self.File_name)
            self.End_page = reader.getNumPages()
        print("Start to cut pages, cut pages from %d to %d..." % (self.Start_page, self.End_page))
        fp = PdfFileReader(open(filename, 'rb'))
        output = PdfFileWriter()
        for i in range(self.Start_page-1, self.End_page):
            output.addPage(fp.getPage(i))
        output_filename = "output.pdf"
        output_stream = open(output_filename, "wb")
        output.write(output_stream)
        return output_filename

    def parse(self):
        '''
        :param fn: 要处理的pdf文件名，格式为："filename.pdf"
        :param start_page: 截取的开始页：不大于pdf总页数的整数
        :param end_page: 截取的截止页：不大于pdf总页数，不小于start_page的整数
        :return: 以txt格式文件返回抽取出的文本内容，方便下一步处理,格式为："filename_extracted.txt"
        '''

        cut_file_name = ExtractText.cut_pages(self)  # 要截取的页数，起始页到结束页
        print("Cut pages done.")
        print("Start to extract text...")
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
                            '''写入方式为连续写入，因此对同一文件重复操作时需要删除上一次产生的文件'''
                            f.write(out.get_text() + "\n")
        fn.close()
        print("Extract text done")
        os.remove(cut_file_name)  # 删除中间文件
        return out_extract_name


    def txt_clean(self, file_name):
        # 读取并分词
        with open(file_name, "r", encoding="utf-8") as text:
            words_list = nltk.word_tokenize("".join(text.readlines()))  # 英文分词工具
        print("Start organizing data...")
        punctuation_list = [',', '.', ':', ';', '?', '(', ')', '[', ']', ' .',
                            '&', '!', '*', '@', '#', '$', '%', '-', '®', '\"', '•', '§',
                            'A', 'B', 'C', 'D', 'E', 'F', 'G',
                            'H', 'I', 'J', 'K', 'L', 'M', 'N',
                            'O', 'P', 'Q', 'R', 'S', 'T',
                            'U', 'V', 'W', 'X', 'Y', 'Z']  # 要去除的单个字符，标点符号
        # 去停词和标点符号
        filter_words = [word for word in words_list
                        if word not in list(set(nltk.corpus.stopwords.words("english")))
                        and word not in punctuation_list]
        print("Remove stop words done")
        # 词形还原
        wordnet_le = nltk.stem.WordNetLemmatizer()
        lemmatize_words = [wordnet_le.lemmatize(word) for word in filter_words]
        print("Words Lemmatizer done")

        # 整理为字符串
        cleaned_string = (" ".join(lemmatize_words)).lower()

        # 用正则表达式去除特殊字符
        pattern = ["\\d", "\\.", "§"]
        for i in range(len(pattern)):
            cleaned_string = re.sub(pattern[i], "", cleaned_string)

        out_cleaned_name = "".join(file_name.split(".")[:-1]) + '_' + 'cleaned.txt'  # 处理产生的文件名
        with open(out_cleaned_name, "w", encoding="utf-8") as writer:
            writer.write(cleaned_string)
        print("Organizing data done")
        return out_cleaned_name


if __name__ == '__main__':
    filename = "pdf_reference_17.pdf"   # 要抽取的文件名
    time1 = time.time()

    extract = ExtractText(filename)

    extracted_file_name = extract.parse()   # 返回产生的txt文件名，便于下一步处理
    cleaned_file_name = extract.txt_clean(extracted_file_name)  # 对抽取出的文件进行整理

    time2 = time.time()
    print("Total time :%fs" % (time2 - time1))
