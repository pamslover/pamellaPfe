import yake
from yake.highlight import TextHighlighter


class Keywords:

    def __init__(self):
        '''
        this is the test of my bla bla car
        '''
        self.text = None
        self.lang = "french"
        self.windowSize = 1
        self.array_of_keywords = []
        self.numOfKeywords = 50
        self.max_ngram_size = 3
        self.deduplication_thresold = 0.9
        self.deduplication_algo = 'seqm'

    def override(self,text=None,language="french", num_of_keywords=50, max_ngram_size=3, deduplication_thresold=0.9):
        self.text = text
        self.lang = language
        self.numOfKeywords = num_of_keywords
        self.max_ngram_size = max_ngram_size
        self.deduplication_thresold = deduplication_thresold
        custom_kw_extractor = yake.KeywordExtractor(lan=self.lang, n=self.max_ngram_size, dedupLim=self.deduplication_thresold,
                                                    dedupFunc=self.deduplication_algo, windowsSize=self.windowSize,
                                                    top=self.numOfKeywords, features=None)
        self.array_of_keywords = custom_kw_extractor.extract_keywords(text)
        return self.array_of_keywords
