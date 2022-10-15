from pydoc import text
import unidecode
import re


class Cleaner:

    def __init__(self) -> None:
        pass

    @staticmethod
    def clean_text(sentence: str):
        sentence = sentence.lower()
        sentence = Cleaner.remove_special_char(Cleaner.extract_only_text(sentence))
        return Cleaner.remove_double_space(sentence)

    @staticmethod
    def remove_double_space(sentence):
        return re.sub(r'([\s])\1{1,}|([\.])\1{1,}', r'\1', str(sentence))

    @staticmethod
    def extract_only_text(sentence):
        sentence = re.sub(r'\S*www\S*\s?', ' ', str(sentence))
        sentence = re.sub(r'\S*http\S*\s?', ' ', sentence)
        sentence = re.sub(r'#^[a-zA-Z-]+@[a-zA-Z-]+\.[a-zA-Z]{2,6}$#', ' ', str(sentence))
        # text = re.sub('(\d+\.)+\d*.*','',str(text))
        sentence = re.sub('\d+', ' ', str(sentence))
        sentence = re.sub("-|_|\t", ' ', str(sentence))
        sentence = re.sub('\n|\r', ' ', str(sentence))
        sentence = re.sub(r'\x00|\uf001', 'fi', str(sentence))
        sentence = re.sub(r'cv', ' ', str(sentence))
        # sentence = re.sub(r'@[A-Za-z0-9]+', '', str(sentence))
        sentence = re.sub(r'[0-9]+', ' ', str(sentence))
        sentence = re.sub(r'\x0c', ' ', str(sentence))
        sentence = re.sub(r'curriculum vitae|nom|prenom|adresse|langue', ' ', str(sentence))
        # text= re.sub(r'[^www]?[A-Za-z] ','',text)
        sentence = re.sub(r'www[a-z0-9\.\-+_]+\.[a-z]+[/-][a-zA-Z]?[a-z\-]+', r' ', str(sentence))
        sentence = re.sub(r'\uf005|\uf006|\uf10b|\ue81e|\ue811|\ue80d|\ue81a|\ue803', r' ', str(sentence))

        return sentence

    @staticmethod
    def remove_special_char(sentence: str):
        return re.sub(r"[^a-zA-Z0-9\-“”\s\'\.]", " ", str(sentence))
