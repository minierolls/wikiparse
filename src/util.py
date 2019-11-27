from html.parser import HTMLParser
import os
import unicodedata

import spacy
import numpy as np

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow
import tensorflow_hub
import tensorflow_text


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
        self.embeddings_model = tensorflow_hub.load(
            "https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/2"
        )

    def open_utf_file(self, file_path):
        """
        Open a UTF-8 encoded file and normalize.

        Args:
            file_path: Path to UTF-8 encoded file

        Returns:
            String representation of file
        """
        try:
            f = open(file_path, "r", encoding="utf-8")
            file_str = unicodedata.normalize("NFKD", f.read().strip())
            f.close()
        except:
            print("Failed to open file " + file_path)
            return False
        return file_str

    def load_html_article(self, article_path):
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
        article_str = self.open_utf_file(article_path)

        if not article_str:
            return False

        parser = ArticleParser()
        parser.feed(article_str)

        return parser.parsed_content

    def load_txt_article(self, article_path):
        """
        Load and return an article saved in TXT format. Content stored in the
        article will be categorized by recognized patterns with HTML tags.

        Args:
            article_path: Path to article TXT file

        Returns:
            [(HTML Tag, Enclosed Text), (HTML Tag, Enclosed Text), ...] or False
        """
        article_str = self.open_utf_file(article_path)

        if not article_str:
            return False

        article_out = []

        # First line assumed to be article title
        article_out.append(("h1", article_str.splitlines()[0]))

        # Categorize article lines as paragraph or section header
        for line in article_str.splitlines()[1:]:
            if "." in line or "," in line:
                article_out.append(("p", line))
            else:
                article_out.append(("h2", line))
            # All content after "References" header is considered irrelevant
            if line.lower() == "references" or line.lower() == "see also":
                break

        return article_out

    def embeddings(self, sentences):
        """
        Return word embeddings for provided sequence of tokens.

        Args:
            sentence: A sentence string for which to find word embeddings

        Returns:
            Word embeddings of provided sentence as NumPy array
        """
        tensors = self.embeddings_model(sentences)["outputs"]

        return tensors


class Article:
    """Structured representation of an article."""

    def __init__(self, article):
        """
        Initializes an Article with the following fields:
            sentences: A list where the ith element is the list of spacy sentences in the ith paragraph
            tokens: a list where the ith element is a list of spacy token lists for the ith paragraph
            entities: a list where the ith element is a list of spacy entities for the ith paragraph.

        Args:
            article: Loaded article from Util.load_article()
        """
        self.nlp = spacy.load("en_core_web_lg")
        self.sentences = []
        self.tokens = []
        self.entities = []
        for element in article:
            if element[0] == "p":
                doc = self.nlp(element[1])
                paragraph_sents = []
                for sent in doc.sents:
                    paragraph_sents.append(sent)
                paragraph_tokens = []
                paragraph_entities = []
                for sentence in paragraph_sents:
                    token = []
                    entities = sentence.ents
                    for word in sentence:
                        token.append(word)
                    paragraph_tokens.append(token)
                    paragraph_entities.append(entities)
                self.sentences.append(paragraph_sents)
                self.tokens.append(paragraph_tokens)
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
                if token in sentence.text:
                    out_list.append((paragraph_index, sentence_index, sentence.text))

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
                    if entity.label_ == entity_type and entity.text not in out_list:
                        out_list.append(entity.text)
        return out_list


if __name__ == "__main__":
    util = Util()
    parsed_article = util.load_txt_article("../articles/Development_data/set1/set1/a1.txt")
    f = open("a1.txt", "w", encoding="utf-8")
    for segment in parsed_article:
        f.write(segment[1])
