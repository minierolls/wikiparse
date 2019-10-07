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
	"""
	Initializes an Article with the following fields:
	sentences: A list where the ith element is the list of sentences in the ith paragraph
	tokens: a list where the ith element is a list of token lists for the ith paragraph
	tagged_tokens: a list where the ith element is a list of tagged token lists for the ith paragraph.
		       A tagged token is a tuple of the form (token, tag)
	entities: a list where the ith element is a list of entity lists for the ith paragraph.
		  A entity is a tuple of the form (token, label)
	"""
	self.sentences = []
	self.tokens = []
	self.tagged_tokens = []
	self.entities = []
	for element in article:
		if element[0] == 'p':
			paragraph_sents = nltk.sent_tokenize(element[1])
			paragraph_tokens = []
			paragraph_tagged_tokens = []
			paragraph_entities = []
			for sentence in paragraph_sents:
				token = nltk.word_tokenize(sentence)
				tagged_token = nltk.pos_tag(token)
				entity = nltk.chunk.ne_chunk(tagged_token)
				paragraph_tokens.append(token)
				paragraph_tagged_tokens.append(tagged_token)
				entity_list = []
				for chunk in entity:
					if hasattr(chunk, 'label'):
						entity_list.append((' '.join(c[0] for c in chunk), chunk.label()))
				paragraph_entities.append(entity_list)
			self.sentences.append(paragraph_sents)
			self.tokens.append(paragraph_tokens)
			self.tagged_tokens.append(paragraph_tagged_tokens)
			self.entities.append(paragraph_entities)

        return


if __name__ == "__main__":
    pass
