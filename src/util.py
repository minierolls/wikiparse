import nltk
import tensorflow
import tensorflow_hub


class Util:
    def __init__(self):
        self.embeddings_model = tensorflow_hub.Module(
            "https://tfhub.dev/google/elmo/2", trainable=False
        )
        return

    def load_article(self, article_path):
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

    def embeddings(self, tokens_sequence):
        """
        Return word embeddings for a provided sequence of tokens.
        """
        tokens_length = len(tokens_sequence)
        return self.embeddings_model(
            inputs={"tokens": tokens_sequence, "sequence_len": tokens_length},
            signature="tokens",
            as_dict=True,
        )["elmo"]


class Article:
    def __init__(self, article):
        self.tokens = nltk.word_tokenize(article)
        self.tagged_tokens = nltk.pos_tag(self.tokens)
        self.entities = nltk.chunk.ne_chunk(self.tagged_tokens)

        return


if __name__ == "__main__":
    pass
