from langid.langid import LanguageIdentifier, model


class LanguageCheck:

    def __init__(self):
        self.text = None
        self.language = None

    def override(self, text):
        self.text = text
        identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
        self.language = identifier.classify(self.text)

        return self.language

    @property
    def text(self):
        return self.text

    @property
    def language(self):
        return self.language
