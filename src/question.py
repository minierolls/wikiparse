def generate_questions(article):
    questions = []
    for i in range(len(article.entities)):
        paragraph_entity = article.entities[i]
        for j in range(len(paragraph_entity)):
            sentence_entity = article.entities[i][j]
            people = []
            for entity in sentence_entity:
                if entity[1] == "PERSON":
                    people.append(entity[0]
            sentence = article.sentences[i][j]
            tagged_tokens = data.tagged_tokens[i][j]
            for person in people:
                ind = sentence.find(person)
                next_word_start = ind + len(person) + 1
                next_word_end = sentence.find(" ", next_word_start)
                next_word = sentence[next_word_start:next_word_end]
                can_replace = False
                for tagged_token in tagged_tokens:
                    if tagged_token[0] == next_word and tagged_token[1].startswith("VB"):
                        can_replace = True
                if can_replace:
                    questions.append(sentence[ind:].replace(person, "Who", 1).replace(".", "?"))
    return questions

class Question:
    pass
