from decl_conj import DECL_CONJ_FOLDER
import os
import json
from utils.functions import is_capitalized, capitalize
import random

NOUNS_FILEPATH = os.path.join(DECL_CONJ_FOLDER, 'decl_conj.json')
PATH_TO_SENTENCES = os.path.join(os.path.dirname(__file__), 'sentences.txt')


def get_wrong_forms(word_data: dict[str, list[str]], english: str, correct_form: str) -> list[str]:
    available_forms = [word for word in word_data[english] if word.lower() != correct_form.lower()]
    wrong_forms = random.sample(available_forms, 3)
    if is_capitalized(correct_form):
        return [capitalize(w) for w in wrong_forms]
    else:
        return wrong_forms


def build_question(qn_text: str, correct_form: str, wrong_forms: list[str]) -> dict[str, str]:
    qn_data: dict[str, str] = {'qn_text': qn_text}
    correct_choice = random.randint(1, 4)
    available_wrong = wrong_forms.copy()
    for i in range(1, 5):
        if i == correct_choice:
            qn_data['correct'] = str(i)
            qn_data[str(i)] = correct_form
        else:
            wrong_word = random.choice(available_wrong)
            available_wrong.remove(wrong_word)
            qn_data[str(i)] = wrong_word
    return qn_data

