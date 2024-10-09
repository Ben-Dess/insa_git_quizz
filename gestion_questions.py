import json

class Question:
    def __init__(self, idQuest,  question, answers, category, difficulty):
        self.id = idQuest
        self.question = question
        self.answers = answers
        self.category = category
        self.difficulty = difficulty

    def __str__(self):
        return f"{self.question} - {self.answers} - {self.category} - {self.difficulty}"

def get_questions():
    with open("questions.json", "r") as file:
        questions = json.load(file)
        questions_list = []
        for question in questions["questions"]:
            questions_list.append(Question(question["id"], question["question"], question["answers"], question["category"], question["difficulty"]))
        return questions_list
    
def get_question_by_id(id):
    questions = get_questions()
    for question in questions:
        if question.id == id:
            return question
    return None

def get_questions_by_category(category):
    questions = get_questions()
    questions_by_category = []
    for question in questions:
        if question.category == category:
            questions_by_category.append(question)
    return questions_by_category

def get_questions_by_difficulty(difficulty):
    questions = get_questions()
    questions_by_difficulty = []
    for question in questions:
        if question.difficulty == difficulty:
            questions_by_difficulty.append(question)
    return questions_by_difficulty

print(get_questions())