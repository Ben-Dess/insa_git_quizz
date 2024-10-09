import json
import random

class Question:
    def __init__(self, idQuest,  question, answers, category, difficulty):
        self.id = idQuest
        self.question = question
        self.answers = answers
        self.category = category
        self.difficulty = difficulty
    
    def getanswers(self):
        answers = []
        for answer in self.answers:
            if answer["isCorrect"]:
                answers.append(answer)
        for i in range(3):
            random_answer = random.choice(self.answers)
            if random_answer not in answers:
                answers.append(random_answer)
        random.shuffle(answers)
        return answers
    
    def check_answer(self, answer):
        for ans in self.answers:
            if ans["text"] == answer:
                return ans["isCorrect"]
        return False

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
    for question in questions:
        print(question.question)

    
def get_random_question(questions):
    return random.choice(questions)

def main():
    questions = get_questions()
    for question in questions:
        print(question.question)
        reponses = question.getanswers()
        for answer in reponses:
            print(f"{reponses.index(answer)+1}. {answer['text']}")
        choice = input("Entre ta réponse: ")
        if question.check_answer(reponses[int(choice)-1]):
            print("Correct")
        else:
            print("Incorrect")

if __name__ == "__main__":
    main()