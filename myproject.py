#!/usr/bin/env python
#data:2019/7/18
#author:xiaojiu

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter,PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from PyPDF2 import PdfFileWriter, PdfFileReader
import time
import os

time1 = time.time()

def cut_pages(filename,start_page, end_page):
    '''
    :param filename: 要处理的pdf文件名，格式为："filename.pdf"
    :param start_page: 截取的开始页：不大于pdf总页数的整数
    :param end_page: 截取的截止页：不大于pdf总页数，不小于start_page的整数
    :return: 返回截取后的pdf文件名，格式为："output_filename.pdf"（这是一个中间值，整体运行结束之后会被删除）
    '''

    fp = PdfFileReader(open(filename,'rb'))
    output = PdfFileWriter()
    for i in range(start_page-1,end_page):
        output.addPage(fp.getPage(i))
    output_filename = "" .join(filename.split(".")[:-1]) + '_' + 'cut.pdf'
    outputStream = open(output_filename,"wb")
    output.write(outputStream)
    return output_filename

def parse(fn, start_page = 1, end_page = None):
    '''
    :param fn: 要处理的pdf文件名，格式为："filename.pdf"
    :param start_page: 截取的开始页：不大于pdf总页数的整数
    :param end_page: 截取的截止页：不大于pdf总页数，不小于start_page的整数
    :return: 以txt格式文件返回抽取出的文本内容，方便下一步处理,格式为："out_name.txt"
    '''
    # 如果没有给出截取的页数，则默认全部抽取
    if end_page == None:
        reader = PdfFileReader(fn)
        page_number = reader.getNumPages()
        end_page = page_number

    cut_file_name = cut_pages(fn,start_page,end_page) #要截取的页数，起始页到结束页

    # 抽取截取过的pdf文件的文本内容
    fn = open(cut_file_name, 'rb')
    parser = PDFParser(fn)  #创建pdf文档分析器
    pdfdoc = PDFDocument()     #创建pdf文档对象
    # 连接分析器和文档
    parser.set_document(pdfdoc)
    pdfdoc.set_parser(parser)
    # 初始化文档
    pdfdoc.initialize("")
    out_extract_name = "" .join(filename.split(".")[:-1]) + '_' + 'extracted.txt'  #抽取出的txt文件名
    if not pdfdoc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        resource = PDFResourceManager() #创建pdf资源管理器
        laparams = LAParams()   #创建pdf参数分析器
        device = PDFPageAggregator(resource, laparams=laparams) #创建聚合器
        interpreter = PDFPageInterpreter(resource, device)  #创建pdf页面对象解释器

        for page in pdfdoc.get_pages():
            #使用界面解释器读取内容
            interpreter.process_page(page)
            #使用聚合器获取内容
            layout = device.get_result()
            for out in layout:
                if hasattr(out, "get_text"):
                    with open(out_extract_name, 'a', encoding="utf-8") as f:
                        f.write(out.get_text())
    fn.close()
    os.remove(cut_file_name)  # 删除中间文件

    return out_extract_name

if __name__ == '__main__':
    fn_path = r"C:\Users\Admin\PycharmProjects\pdf_ex\extract_pdf_file\\"  #要抽取的文件所在路径
    fn = r"acrobat-xi-pdf-accessibility-overview_decrypted.pdf"   #要抽取的文件名
    filename = fn_path + fn
    extracted_file_name = parse(filename,1,2)   #返回产生的txt文件名，便于下一步处理
    # print(extracted_file_name)
    time2 = time.time()
    print("总时间:%fs" %(time2 - time1))