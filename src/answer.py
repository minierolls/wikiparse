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

    def answer(self, question, return_score=False):
        """
        Answer the given question.

        Args:
            question: Question string

        Returns:
            Answer to question as string
        """
        u = Util()
        question_embedding = u.embeddings([question])[0]

        sentences_list = []

        for paragraph in self.article.sentences:
            paragraph_text = [s.text for s in paragraph]
            sentences_list += paragraph_text

        sentences_embeddings = u.embeddings(sentences_list)

        distances = []
        for i, embedding in enumerate(sentences_embeddings):
            diffs = np.inner(question_embedding, embedding)
            dist = diffs

            distances.append((dist, sentences_list[i]))

        distances.sort(key=lambda x: x[0], reverse=True)

        most_similar_sentence = distances[0][1]
        most_similar_score = distances[0][0]

        if return_score:
            return (most_similar_sentence, most_similar_score)

        return most_similar_sentence


if __name__ == "__main__":
    u = Util()
    art = Article(u.load_txt_article("../articles/Development_data/set4/set4/a1.txt"))
    a = Answer(art)
    q = "Who studied the stars of the southern hemisphere from 1750 until 1754 from Cape of Good Hope?"
    print(a.answer(q))

# Who is a product of a revision of the Old Babylonian system in later Neo-Babylonian astronomy 6th century BC?
# Who interpreted the creatures appearing in the books of Ezekiel (and thence in Revelation) as the middle signs of the four quarters of the Zodiac?
# Who studied the stars of the southern hemisphere from 1750 until 1754 from Cape of Good Hope?
# Who aided the IAU (International Astronomical Union) in dividing the celestial sphere into 88 official constellations?
# Who is a product of a revision of the Old Babylonian system in later Neo-Babylonian astronomy 6th century BC?
