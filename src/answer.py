import nltk
import numpy as np

from util import Util, Article


class Answer:
    """Answer questions based on the initialized article."""

    def __init__(self, article):
        """
        Create a new instance of the Answer class.

        Args:
            article: An instance of the Article class
        """
        self.article = article

    def answer(self, question):
        """
        Answer the given question.

        Args:
            question: Question string

        Returns:
            Answer to question as string
        """
        question_embedding = u.embeddings([question])[0]

        sentences_list = []

        for paragraph in art.sentences:
            sentences_list += paragraph

        sentences_embeddings = u.embeddings(sentences_list)

        distances = []
        for i, embedding in enumerate(sentences_embeddings):
            diffs = question_embedding - embedding
            dist = sum(np.abs(diffs))

            distances.append((dist, sentences_list[i]))

        distances.sort(key=lambda x: x[0])

        return distances[0][1]


if __name__ == "__main__":
    u = Util()
    art = Article(u.load_txt_article("articles/Development_data/set1/set1/a1.txt"))
    a = Answer(art)
    q = "Who was the next great pyramid builder?"
    print(a.answer(q))
