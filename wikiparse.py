from src.answer import Answer
from src.question import Question
from src.util import Article, Util


def ask(article_path, num_questions):
    u = Util()
    q = Question(u.load_txt_article(article_path))
    questions = q.generate(num_questions)
    for question in questions:
        print(question)


def answer(article_path, questions_path):
    u = Util()
    a = Answer(u.load_txt_article(article_path))
    q = u.open_utf_file(questions_path)
    q = q.splitlines()
    for question in q:
        print(a.answer(question))
