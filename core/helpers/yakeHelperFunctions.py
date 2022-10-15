import yake
from nltk.tokenize import RegexpTokenizer
from tqdm import tqdm


def keywords_yake(sample_posts):
    # take keywords for each post & turn them into a text string "sentence"
    # create empty list to save our "sentences" to
    simple_kw_extractor = yake.KeywordExtractor()
    sentences = []
    for post in sample_posts:
        post_keyword = simple_kw_extractor.extract_keywords(post)
        sentence_output = ""
        for word, number in post_keyword:
            sentence_output += word + " "
        sentences.append(sentence_output)
    return sentences

    # use the sentences as input for brown clustering


def tokenizing_after_yake(sentences):
    # tokenize
    tokenizer = RegexpTokenizer(r'\w+')
    sample_data_tokenized = [w.lower() for w in sentences]
    sample_data_tokenized = [tokenizer.tokenize(i) for i in sample_data_tokenized]
    return sample_data_tokenized


class YakeHelperFunctions:

    def get_cluster_maybe(self, megacluster):
        cluster_list = [[]]
        list_index = 0
        for i in range(len(megacluster) - 1):
            if megacluster[i] < megacluster[i + 1]:
                cluster_list[list_index].append(megacluster[i])
            else:
                cluster_list[list_index].append(megacluster[i])
                list_index = list_index + 1
                cluster_list.append([])
        return cluster_list
