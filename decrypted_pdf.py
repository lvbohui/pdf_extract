#!/usr/bin/env python
import time
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter

def get_reader(filename, password):
    try:
        old_file = open(filename, 'rb')
        print("run decrypte 2")
    except Exception as err:
        print("Error! "+str(err))
        return None

    pdf_reader = PdfFileReader(old_file,strict=False)
    if pdf_reader.isEncrypted:
        if password is None:
            print("%s文件被加密，需要密码！"%filename)
            return None
        else:
            if pdf_reader.decrypt(password) != 1:
                print("%s密码不正确！"%filename)
                return None
    if old_file in locals():
        old_file.close()
    return pdf_reader
def decrtpt_pdf(path, filename, password, decrypted_filename = None):
    print("run decrypte 1")
    filename_inside = path + filename
    pdf_reader = get_reader(filename_inside, password)
    if pdf_reader is None:
        return
    if not pdf_reader.isEncrypted:
        print("文件没有被加密，无需操作！")
        return
    pdf_writer = PdfFileWriter()
    pdf_writer.appendPagesFromReader(pdf_reader)
    if decrypted_filename is None:
        decrypted_filename = "" .join(filename.split(".")[:-1]) + '_' + 'decrypted.pdf'
        print(decrypted_filename)
    pdf_writer.write(open(decrypted_filename ,'wb'))

if __name__ == "__main__":
    time_start = time.time()
    read_path = r"H:\Project\local_project\grpc-learn\pdf_file"
    fn = r"\Acme Corporation Inc NDA template.pdf"
    decrtpt_pdf(read_path, fn,'')
    time_end = time.time()
    print("总共消耗时间：", (time_end - time_start))