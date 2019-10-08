from html.parser import HTMLParser
import unicodedata

import nltk
import tensorflow
import tensorflow_hub


class ArticleParser(HTMLParser):
    """An extension of the Python HTMLParser to parse articles."""

    def __init__(self):
        """
        Create a new instance of the ArticleParser class.
        """
        super(ArticleParser, self).__init__()
        self.parse_tags = ["h1", "h2", "h3", "title", "p", "li"]
        self.remove_tags = ["b", "i", "span", "cite"]

        self.current_tag = None

        self.parsed_content = []
        self.parse_index = 0

    def reset(self):
        """
        Reset this instance. Loses all unprocessed data and parsed content.
        """
        super(ArticleParser, self).reset()
        self.parsed_content = []
        self.current_tag = None
        self.parse_index = 0

    def handle_starttag(self, tag, attributes):
        if tag in self.parse_tags:
            self.current_tag = tag
            self.parse_index += 1

    def handle_endtag(self, tag):
        if tag == self.current_tag:
            self.current_tag = None

    def handle_data(self, data):
        if self.parse_index >= len(self.parsed_content):
            self.parsed_content.append((self.current_tag, ""))

        current_tag_content = self.parsed_content[self.parse_index]
        current_tag_content = (current_tag_content[0], current_tag_content[1] + data)
        self.parsed_content[self.parse_index] = current_tag_content


class Util:
    """Collection of useful functionality."""

    def __init__(self):
        """
        Create a new instance of the Util class.
        """
        tensorflow.compat.v1.disable_eager_execution()
        self.embeddings_model = tensorflow_hub.Module(
            "https://tfhub.dev/google/elmo/2", trainable=False
        )

    def load_article(self, article_path):
        """
        Load and return an article saved in HTML format.
        Only the following tags will be parsed:
            <h1>
            <h2>
            <h3>
            <title>
            <p>
            <li>

        The following HTML tags will be ignored but enclosed text will be
        added to the parent HTML tag:
            <b>
            <i>
            <span>
            <cite>

        All other HTML tags (and enclosed content) will be ignored.

        Args:
            article_path: Path to article HTML file

        Returns:
            [(HTML Tag, Enclosed Text), (HTML Tag, Enclosed Text), ...] or False
        """
        try:
            f = open(article_path, "r", encoding="utf-8")
            article_str = unicodedata.normalize("NFKD", f.read().strip())
            f.close()
        except:
            return False

        parser = ArticleParser()
        parser.feed(article_str)

        return parser.parsed_content

    def embeddings(self, tokens_sequence):
        """
        Return word embeddings for a provided sequence of tokens.

        Args:
            tokens_sequence: A list of tokens for which to find word embeddings

        Returns:
            Word embeddings of provided token sequence
        """
        tokens_length = len(tokens_sequence)
        return self.embeddings_model(
            inputs={"tokens": tokens_sequence, "sequence_len": tokens_length},
            signature="tokens",
            as_dict=True,
        )["elmo"]


class Article:
    """Structured representation of an article."""

    def __init__(self, article):
        """
        Initializes an Article with the following fields:
            sentences: A list where the ith element is the list of sentences in the ith paragraph
            tokens: a list where the ith element is a list of token lists for the ith paragraph
            tagged_tokens: a list where the ith element is a list of tagged token lists for the ith paragraph.
                    A tagged token is a tuple of the form (token, tag)
            entities: a list where the ith element is a list of entity lists for the ith paragraph.
                A entity is a tuple of the form (token, label)

        Args:
            article: Loaded article from Util.load_article()
        """
        nltk.download("punkt")
        nltk.download("averaged_perceptron_tagger")
        nltk.download("maxent_ne_chunker")
        nltk.download("words")

        self.sentences = []
        self.tokens = []
        self.tagged_tokens = []
        self.entities = []
        for element in article:
            if element[0] == "p":
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
                        if hasattr(chunk, "label"):
                            entity_list.append(
                                (" ".join(c[0] for c in chunk), chunk.label())
                            )
                    paragraph_entities.append(entity_list)
                self.sentences.append(paragraph_sents)
                self.tokens.append(paragraph_tokens)
                self.tagged_tokens.append(paragraph_tagged_tokens)
                self.entities.append(paragraph_entities)

    def search_token(self, token):
        """
        Returns a list of all sentences that contain the provided token.

        Args:
            token: A string query token

        Returns:
            A list of tuples of the form (par_index, sent_index, sentence)
            where par_index is the index of the paragraph, sent_index is the
            index of the sentence, and sentence is the string sentence.
        """
        out_list = []

        for paragraph_index, paragraph in enumerate(self.sentences):
            for sentence_index, sentence in enumerate(paragraph):
                if token in sentence:
                    out_list.append((paragraph_index, sentence_index, sentence))

        return out_list

    def get_entities_of_type(self, entity_type):
        """
        Returns all entities of a specified type.

        Args:
            entity_type: Entity type string

        Returns:
            List of entities as strings
        """
        out_list = []

        for paragraph in self.entities:
            for sentence in paragraph:
                for entity in sentence:
                    if entity[1] == entity_type and entity[0] not in out_list:
                        out_list.append(entity[0])
        return out_list


if __name__ == "__main__":
    util = Util()
    parsed_article = util.load_article("articles/Development_data/set1/set1/a1.htm")
    f = open("a1.txt", "w", encoding="utf-8")
    for segment in parsed_article:
        f.write(segment[1])
