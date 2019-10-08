from util import Article, Util


class Question:
    """Generate questions from the initialized article."""

    def __init__(self, article):
        """
        Create a new instance of the Question class.

        Args:
            article: An instance of the Article class
        """
        self.article = article

    def generate(self, num_questions):
        """
        Generate desired number of questions.

        Args:
            num_questions: Number of questions to generate

        Returns:
            List of questions as strings
        """
        questions = []
        for i in range(len(self.article.entities)):
            paragraph_entity = self.article.entities[i]
            for j in range(len(paragraph_entity)):
                sentence_entity = self.article.entities[i][j]
                people = []
                for entity in sentence_entity:
                    if entity[1] == "PERSON":
                        people.append(entity[0])
                sentence = self.article.sentences[i][j]
                tagged_tokens = self.article.tagged_tokens[i][j]
                for person in people:
                    ind = sentence.find(person)
                    next_word_start = ind + len(person) + 1
                    next_word_end = sentence.find(" ", next_word_start)
                    next_word = sentence[next_word_start:next_word_end]
                    can_replace = False
                    for tagged_token in tagged_tokens:
                        if tagged_token[0] == next_word and tagged_token[1].startswith(
                            "VB"
                        ):
                            can_replace = True
                    if can_replace:
                        questions.append(
                            sentence[ind:].replace(person, "Who", 1).replace(".", "?")
                        )
        if len(questions) < num_questions:
            questions += questions[0 : num_questions - len(questions)]

        return questions[0:num_questions]


if __name__ == "__main__":
    u = Util()
    a = Article(u.load_article("articles/Development_data/set1/set1/a1.htm"))
    q = Question(a)
    print(q.generate(5))
