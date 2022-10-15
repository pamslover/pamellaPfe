from nltk.corpus import stopwords
from core.languageCheck.languageCheck import LanguageCheck
import spacy

fr_nlp = spacy.load("fr_core_news_md")
en_nlp = spacy.load("en_core_web_md")


class process:

    def __init__(self):
        self.lang = 'fr'

    def Lang(self, text):
        self.lang = LanguageCheck().override(text)
        if self.lang in 'en':
            x = en_nlp(text)
        else:
            x = fr_nlp(text)
        return x

    @staticmethod
    def _tokenization(text, all_pos=False) :
        # text = cleaner.clean_text(text)
        doc = process().Lang(text)
        if not all_pos:
            pos_tag = ['PRON', 'ADJ', 'NOUN', 'VERB', "ADV"]
            return [token for token in doc if not token.is_stop and len(token) > 1 and token.pos_ in pos_tag]
        return [token for token in doc if not token.is_stop and len(token) > 1]

    @staticmethod
    def _tokens(doc):
        return [token.text for token in doc]

    @property
    def tokens(self, text, all_pos=False):
        tokens = self._tokenization(text, all_pos)
        return self._tokens(tokens)

    @property
    def lemma(self, text, all_pos):
        tokens = self._tokenization(text, all_pos)
        return [tok.lemma_.lower() for tok in tokens]
