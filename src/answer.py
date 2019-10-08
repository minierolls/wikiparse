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
        pass
