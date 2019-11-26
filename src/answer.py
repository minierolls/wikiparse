import numpy as np

from src.util import Util, Article


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
        u = Util()
        question_embedding = u.embeddings(question)[0]

        sentences_list = []

        for paragraph in self.article.sentences:
            paragraph_text = [s.text for s in paragraph]
            sentences_list += paragraph_text

        sentences_embeddings = []
        for sentence in sentences_list:
            sentences_embeddings.append(u.embeddings(sentence)[0])

        distances = []
        for i, embedding in enumerate(sentences_embeddings):
            denom = question_embedding.size * embedding.size
            diffs = np.dot(question_embedding, embedding.T) / denom
            dist = np.average(diffs)

            distances.append((dist, sentences_list[i]))

        distances.sort(key=lambda x: x[0])

        return distances[0][1]


if __name__ == "__main__":
    u = Util()
    art = Article(u.load_txt_article("../articles/Development_data/set1/set1/a1.txt"))
    a = Answer(art)
    q = "Who was the next great pyramid builder?"
    print(a.answer(q))
