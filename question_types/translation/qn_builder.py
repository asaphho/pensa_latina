from question_types.translation import TRANSLATION_FOLDER
import os
import json
from typing import Union
import random

latin_to_english_path = os.path.join(TRANSLATION_FOLDER, 'latin_to_english.json')
english_to_latin_path = os.path.join(TRANSLATION_FOLDER, 'english_to_latin.json')


def choose_sentence_and_make_question(sentences: list[dict[str, Union[str, list[str]]]]) -> dict[str, str]:
    sentence_data: dict[str, Union[str, list[str]]] = random.choice(sentences)
    correct: str = sentence_data['correct']
    sentence: str = sentence_data['sentence']
    wrong_sentences: list[str] = [snt for snt in sentence_data['wrong'] if snt != correct]
    question_data = {'qn_text': sentence}
    correct_choice = random.randint(1, 4)
    for i in range(1, 5):
        if i == correct_choice:
            question_data[str(i)] = correct
        else:
            wrong_sentence = random.choice(wrong_sentences)
            wrong_sentences.remove(wrong_sentence)
            question_data[str(i)] = wrong_sentence
    return question_data


def display_question(qn_data: dict[str, str]) -> None:
    print('Translate the following sentence:')
    print(qn_data['qn_text'])
    for i in range(1, 5):
        print(f'{i}: {qn_data[str(i)]}')
    print('\ne: Terminate exercise')


def test_question(qn_data: dict[str, str]) -> bool:
    display_question(qn_data)
    while True:
        player_input = input().strip()
        if player_input == qn_data['correct']:
            print('Correct!')
            return False
        elif player_input in ('1', '2', '3', '4'):
            print(f'Sorry, the answer is "{qn_data[qn_data["correct"]]}"')
            return False
        elif player_input.lower() == 'e':
            print('Exercise terminated.')
            return True
        else:
            print('Unrecognized input. Try again.')


def begin_exercise(from_english: bool = False) -> None:
    filepath = english_to_latin_path if from_english else latin_to_english_path
    with open(filepath, 'r') as f:
        sentences_list = json.load(f)
    exit_loop = False
    while not exit_loop:
        qn = choose_sentence_and_make_question(sentences=sentences_list)
        exit_loop = test_question(qn)
