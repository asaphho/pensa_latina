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


def make_question_from_random_sentence(sentences: list[str], word_forms: dict[str, dict[str, list[str]]]) -> dict[str, str]:
    chosen_sentence = random.choice(sentences)
    split_sections = chosen_sentence.split('/')
    display_sentence = split_sections[0]
    word_sections: list[list[str]] = [part.split('-') for part in split_sections[1:]]
    section_to_test = random.choice(word_sections)
    word_to_test = section_to_test[0]
    word_forms_data = word_forms[section_to_test[1]]
    english = section_to_test[2]
    display_sentence = display_sentence.replace(word_to_test, '______', 1)
    wrong_forms = get_wrong_forms(word_forms_data, english, word_to_test)
    return build_question(display_sentence, word_to_test, wrong_forms)


def display_question(qn_data: dict[str, str]) -> None:
    print('Fill in the blank:')
    print(qn_data['qn_text'])
    for i in range(1, 5):
        print(f'{str(i)}: {qn_data[str(i)]}')
    print('\ne: Exit exercise')


def test_question(qn_data: dict[str, str]) -> bool:
    display_question(qn_data)
    while True:
        player_input = input().strip()
        if player_input == qn_data['correct']:
            print('Correct!')
            return False
        elif player_input in ('1', '2', '3', '4'):
            print(f'Sorry, the answer is "{qn_data[qn_data["correct"]]}".')
            return False
        elif player_input.lower() == 'e':
            print('Exercise terminated.')
            return True
        else:
            print('Unrecognized input. Try again.')


def begin_exercise(no_repeat: int = 10):
    with open(PATH_TO_SENTENCES, 'r') as f:
        lines = f.readlines()
    sentences = [ln.strip() for ln in lines if ln.strip() != '']
    nouns_adjs_path = os.path.join(DECL_CONJ_FOLDER, 'nouns_adjs.json')
    verbs_path = os.path.join(DECL_CONJ_FOLDER, 'verbs.json')
    with open(nouns_adjs_path, 'r') as f:
        nouns_adjs: dict[str, list[str]] = json.load(f)
    with open(verbs_path, 'r') as f:
        verbs: dict[str, list[str]] = json.load(f)
    exit_loop = False
    cannot_test = []
    while not exit_loop:
        qn = make_question_from_random_sentence(sentences=sentences,
                                                word_forms={'noun': nouns_adjs, 'adjective': nouns_adjs,
                                                            'verb': verbs})
        while qn['qn_text'] in cannot_test:
            qn = make_question_from_random_sentence(sentences=sentences,
                                                    word_forms={'noun': nouns_adjs, 'adjective': nouns_adjs,
                                                                'verb': verbs})
        exit_loop = test_question(qn)
        if len(cannot_test) >= no_repeat:
            cannot_test.pop(0)
        cannot_test.append(qn['qn_text'])
