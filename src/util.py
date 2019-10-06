import nltk


def load_article(article_path):
    """
    Return a string representation of the file at the provided path,
    or return False if operation fails.
    """
    try:
        f = open(article_path, "r")
        out_str = f.read()
        f.close()
        return out_str()
    except:
        return False


class Article:
    def __init__(self, article):

        self.tokens = nltk.word_tokenize(article)
        self.tagged_tokens = nltk.pos_tag(self.tokens)
        self.entities = nltk.chunk.ne_chunk(self.tagged_tokens)

        return
