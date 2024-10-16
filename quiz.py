import sqlite3
from typing import List, Dict
import random
import time

class Question:
    def __init__(self, id: int, idBonneRep: int, question: str, difficulty: str, theme: list, reponses: list):
        self.id = id
        self.question = question
        self.idBonneRep = idBonneRep
        self.difficulty = difficulty
        self.theme = theme
        self.reponses = reponses

    def __str__(self):
        return f"{self.question} ({self.difficulty})"
    
class Reponse:
    def __init__(self, id: int, reponse: str):
        self.id = id
        self.reponse = reponse

    def __str__(self):
        return f"{self.reponse}"
    
class Theme:
    def __init__(self, id: int, theme: str):
        self.id = id
        self.theme = theme

    def __str__(self):
        return f"{self.theme}"

def get_questions_from_db(db_path: str) -> List[Question]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Question")
    questions = []
    for row in cursor.fetchall():
        id, idBonneRep, question, difficulty = row
        questions.append(Question(id, idBonneRep, question, difficulty, [], []))
        cursor.execute("SELECT * FROM QuestionReponses WHERE idQuestion = ?", (str(id),))
        for row in cursor.fetchall():
            _, idReponse = row
            cursor.execute("SELECT * FROM Reponses WHERE idreponse = ?", (str(idReponse),))
            reponse = cursor.fetchone()
            questions[-1].reponses.append(Reponse(reponse[0], reponse[1]))
        cursor.execute("SELECT * FROM ThemeQuestion WHERE idQuestion = ?", (str(id),))
        for row in cursor.fetchall():
            _, idTheme = row
            cursor.execute("SELECT * FROM Thematique WHERE idTheme = ?", (str(idTheme),))
            theme = cursor.fetchone()
            questions[-1].theme.append(Theme(theme[0], theme[1]))
            cursor.execute("SELECT * FROM LiaisonThematique WHERE idTheme1 = ?", (str(idTheme),))
            for row in cursor.fetchall():
                _, idTheme = row
                cursor.execute("SELECT * FROM Thematique WHERE idTheme = ?", (str(idTheme),))
                theme = cursor.fetchone()
                questions[-1].theme.append(Theme(theme[0], theme[1]))
    conn.close()
    return questions

def get_themes_from_db(db_path: str) -> List[Theme]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Thematique")
    themes = []
    for row in cursor.fetchall():
        id, theme = row
        themes.append(Theme(id, theme))
    conn.close()
    return themes

def get_questions_by_theme(questions: List[Question], theme: str) -> List[Question]:
    return [question for question in questions if theme in [t.theme for t in question.theme]]

def get_questions_by_difficulty(questions: List[Question], difficulty: str) -> List[Question]:
    return [question for question in questions if question.difficulty == difficulty]

def get_questions_by_theme_and_difficulty(questions: List[Question], theme: str, difficulty: str) -> List[Question]:
    return [question for question in questions if theme in [t.theme for t in question.theme] and question.difficulty == difficulty]

def get_question_by_id(questions: List[Question], id: int) -> Question:
    return [question for question in questions if question.id == id][0]

def get_reponse_by_id(question: Question, id: int) -> Reponse:
    return [reponse for reponse in question.reponses if reponse.id == id][0]

def get_theme_by_id(question: Question, id: int) -> Theme:
    return [theme for theme in question.theme if theme.id == id][0]

def get_theme_by_name(themes: List[Theme], name: str) -> Theme:
    return [theme for theme in themes if theme.theme == name][0]

def get_theme_id_by_name(themes: List[Theme], name: str) -> int:
    return [theme.id for theme in themes if theme.theme == name][0]

def get_difficulties(questions: List[Question]) -> List[str]:
    return list(set([question.difficulty for question in questions]))

def get_themes(questions: List[Question]) -> List[str]:
    return list(set([theme.theme for question in questions for theme in question.theme]))

def main():
    wrongAnswers = 0
    goodAnswers = 0
    totalScore = 0
    questions = get_questions_from_db("questions.sqlite")
    random.shuffle(questions)
    questions = questions[:10]
    for question in questions:
        print(question)

        # Selectionner 4 réponses avec une bonne réponse
        reponses = question.reponses
        random.shuffle(reponses)
        correct_reponse = get_reponse_by_id(question, question.idBonneRep)
        reponses = reponses[:4]
        if correct_reponse not in reponses:
            reponses[0] = correct_reponse
        random.shuffle(reponses)
        
        for i in range(len(reponses)):
            print(f"{i+1}. {reponses[i]}")

        print()

        repuser = int(input("Votre réponse: ")) - 1
        if reponses[repuser] == correct_reponse:
            print("Bonne réponse")
            goodAnswers += 1
        else:
            print("Mauvaise réponse")
            wrongAnswers += 1
        time.sleep(1.5)
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    total = goodAnswers - wrongAnswers
    print("Vous avez eu",goodAnswers," bonnes réponses,",wrongAnswers,"mauvaises réponses, et un score final de",totalScore) #print score
    

if __name__ == "__main__":
    main()
