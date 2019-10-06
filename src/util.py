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

#sentences is a list where the ith element is a list of the sentences of the ith paragraph in the article
#tokens is a list where each element is the list of tokens from a sentence
#tagged_tokens is a list where each element is a list of tuples of the following form: (token, pos tag) that corresponds to a sentence
#entities is a list where each element is a list of tuples of the following form: (entity, label) that corresponds to a sentence
class Article:
    def __init__(self, article):
	self.sentences = []
	self.tokens = []
	self.tagged_tokens = []
	self.entities = []
	for element in article:
		if element[0] == 'p':
			paragraph_sents = nltk.sent_tokenize(element[1])
			sentences.append(paragraph_sents)
			for sentence in paragraph_sents:
				token = nltk.word_tokenize(sentence)
				tagged_token = nltk.pos_tag(token)
				entity = nltk.chunk.ne_chunk(tagged_token)
				self.tokens.append(token)
				self.tagged_tokens.append(tagged_token)
				entity_list = []
				for chunk in entity:
					if hasattr(chunk, 'label'):
						entity_list.append((' '.join(c[0] for c in chunk), chunk.label()))
				self.entities.append(entity_list)

        return


if __name__ == "__main__":
    pass
