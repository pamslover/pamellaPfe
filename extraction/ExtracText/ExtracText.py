import unicodedata
from io import StringIO
import glob
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import docx2txt
import re


class Extract:

    def __init__(self) -> None:
        pass

    @staticmethod
    def extract_text(filename, pages=None):
        if not pages:
            pagenums = set()
        else:
            pagenums = set(pages)

        output = StringIO()
        # data={}
        content = []
        # name=[]
        # for filename in glob.glob ('/content/drive/MyDrive/CV/*.pdf'):
        with open(filename, 'rb') as in_file:
            if filename.endswith('.docx') or filename.endswith('.doc'):
                text = docx2txt.process(in_file)
                text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf8')
                content = ' '.join([str(elem) for elem in (text.split('\n'))])
                text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf8')
            elif filename.endswith('.pdf'):
                parser = PDFParser(in_file)
                doc = PDFDocument(parser)
                manager = PDFResourceManager()
                converter = TextConverter(manager, output, laparams=LAParams())
                interpreter = PDFPageInterpreter(manager, converter)
                for page in PDFPage.get_pages(in_file, pagenums):
                    interpreter.process_page(page)
                text = output.getvalue()
                text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf8')
                content = ' '.join([str(elem) for elem in (text.split('\n'))])
                in_file.close()
                converter.close()
                output.close()
            else:
                pass
        return content

    @staticmethod
    def extract_number(text):
        numbers = []
        phone = (re.findall(r'\d?[\d(\)]{8,15}\d', str(text)))
        if phone:
            number = ''.join(phone[0])
            if text.find(number) >= 0 and len(number) < 20:
                numbers.append(''.join(str(elem) for elem in number))
        return numbers

    @staticmethod
    def extract_date(text):
        dates = [re.findall(r"\d{1,2}[-/]\d{1,2}[-/]\d{2,4}", str(text)), re.findall(r"\w{4,9} ?\d{2,4}", str(text)),
                 re.findall(r"\d{2,4}''[-/]''\d{2,4}", str(text))]

        return dates


