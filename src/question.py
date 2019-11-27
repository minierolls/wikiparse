from util import Article, Util
from answer import Answer


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

        # Who questions
        people = self.article.get_entities_of_type("PERSON")
        for person in people:
            sentences = self.article.search_token(person)
            for (paragraph_index, sentence_index, sentence) in sentences:
                ind = sentence.find(person)
                next_word_start = ind + len(person) + 1
                next_word_end = sentence.find(" ", next_word_start)
                next_word = sentence[next_word_start:next_word_end]
                tokens = self.article.tokens[paragraph_index][sentence_index]
                can_replace = False
                for token in tokens:
                    if (
                        token.text == next_word
                        and (token.tag_).startswith("VB")
                        and not token.tag_ == "VBG"
                        and not token.tag_ == "VBP"
                    ):
                        can_replace = True
                if can_replace:
                    punctuation = "!\"#&'*+,/:;<=>?@[\\]^_`{|}~"
                    sentence = sentence.translate(
                        str.maketrans(punctuation, "?" * len(punctuation))
                    )
                    s_end = sentence.find("?", ind) + 1
                    question = sentence[ind:s_end].replace(person, "Who", 1)
                    if s_end == 0:
                        question = (
                            sentence[ind:].replace(person, "Who", 1).replace(".", "?")
                        )
                    questions.append(question)

                # Binary questions
                if next_word.lower() == "is" or next_word == "was":
                    punctuation = "!\"#&'*+,/:;<=>?@[\\]^_`{|}~"
                    sentence = sentence.translate(
                        str.maketrans(punctuation, "?" * len(punctuation))
                    )
                    s_end = sentence.find("?", ind) + 1
                    question = sentence[ind:s_end]
                    if s_end == 0:
                        question = sentence[ind:].replace(".", "?")

                    question = question.split()
                    bin_question = []
                    person_ind = None
                    bin_word = None
                    for i, word in enumerate(question):
                        if person_ind is None and word == person:
                            person_ind = i
                        if (
                            person_ind is not None
                            and i == person_ind + 1
                            and (word.lower() == "is" or word.lower() == "was")
                        ):
                            bin_word = word
                            continue
                        bin_question.append(word)
                    if bin_word is not None:
                        bin_question.insert(person_ind, bin_word.title())
                        question = " ".join(bin_question)
                        questions.append(question)

        # What questions
        objects = self.article.get_entities_of_type("EVENT")
        objects += self.article.get_entities_of_type("WORK_OF_ART")
        objects += self.article.get_entities_of_type("FAC")
        objects = list(set(objects))
        for obj in objects:
            sentences = self.article.search_token(obj)
            for (paragraph_index, sentence_index, sentence) in sentences:
                ind = sentence.find(obj)
                next_word_start = ind + len(obj) + 1
                next_word_end = sentence.find(" ", next_word_start)
                next_word = sentence[next_word_start:next_word_end]
                tokens = self.article.tokens[paragraph_index][sentence_index]
                can_replace = False
                for token in tokens:
                    if (
                        token.text == next_word
                        and (token.tag_).startswith("VB")
                        and not token.tag_ == "VBG"
                        and not token.tag_ == "VBP"
                    ):
                        can_replace = True
                if can_replace:
                    punctuation = "!\"#&'*+,/:;<=>?@[\\]^_`{|}~"
                    sentence = sentence.translate(
                        str.maketrans(punctuation, "?" * len(punctuation))
                    )
                    s_end = sentence.find("?", ind) + 1
                    question = sentence[ind:s_end].replace(obj, "What", 1)
                    if s_end == 0:
                        question = (
                            sentence[ind:].replace(obj, "What", 1).replace(".", "?")
                        )
                    questions.append(question)

                # Binary questions
                if next_word.lower() == "is" or next_word == "was":
                    punctuation = "!\"#&'*+,/:;<=>?@[\\]^_`{|}~"
                    sentence = sentence.translate(
                        str.maketrans(punctuation, "?" * len(punctuation))
                    )
                    s_end = sentence.find("?", ind) + 1
                    question = sentence[ind:s_end]
                    if s_end == 0:
                        question = sentence[ind:].replace(".", "?")

                    question = question.split()
                    bin_question = []
                    person_ind = None
                    bin_word = None
                    for i, word in enumerate(question):
                        if person_ind is None and word == person:
                            person_ind = i
                        if (
                            person_ind is not None
                            and i == person_ind + 1
                            and (word.lower() == "is" or word.lower() == "was")
                        ):
                            bin_word = word
                            continue
                        bin_question.append(word)
                    if bin_word is not None:
                        bin_question.insert(person_ind, bin_word.title())
                        question = " ".join(bin_question)
                        questions.append(question)

        # Scoring questions based on answer performance
        a = Answer(self.article)
        question_scores = []
        for question in questions:
            _, score = a.answer(question, return_score=True)
            question_scores.append((question, score))

        question_scores.sort(key=lambda x: x[1], reverse=True)
        questions = [x[0] for x in question_scores]

        while len(questions) < num_questions:
            questions += questions[0 : num_questions - len(questions)]

        return questions[0:num_questions]


if __name__ == "__main__":
    u = Util()
    a = Article(u.load_txt_article("articles/Development_data/set4/set4/a1.txt"))
    q = Question(a)
    print(q.generate(5))
