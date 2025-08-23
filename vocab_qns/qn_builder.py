import os
from vocabulary import VOCABULARY_FOLDER
import random


def open_files(*filenames: str) -> list[str]:
    all_lines = []
    for filename in filenames:
        filepath = os.path.join(VOCABULARY_FOLDER, filename)
        with open(filepath, 'r') as f:
            lines = f.readlines()
        all_lines.extend([ln.strip()for ln in lines if ln.strip() != ''])
    return all_lines


def pick_word_and_ans_choices(lines: list[str], from_english: bool = False) -> dict[str, str]:
    qn_data = {}
    line_to_pick = random.choice(lines)
    word_to_display, answer = line_to_pick.split(' ', maxsplit=1)
    if from_english:
        word_to_display, answer = answer, word_to_display
    choice_index = 0 if from_english else 1
    qn_data['word'] = word_to_display
    qn_data['correct'] = answer
    split_lines: list[list[str]] = [ln.split(' ', maxsplit=1) for ln in lines]
    wrong_choices: list[list[str]] = [ln for ln in split_lines if ln[choice_index] != answer
                                      and ln[1-choice_index] != word_to_display]
    wrong_answers = random.sample(list(set([pair[choice_index] for pair in wrong_choices])), 3)
    for i in range(len(wrong_answers)):
        qn_data[f'wrong{i+1}'] = wrong_answers[i]
    return qn_data


def assign_choices(word_and_choices: dict[str, str]) -> dict[str, str]:
    correct_ans = random.randint(1, 4)
    choice_assignments = {}
    wrong_choices: list[str] = [word_and_choices['wrong1'], word_and_choices['wrong2'], word_and_choices['wrong3']]
    for i in range(1, 5):
        if i == correct_ans:
            choice_assignments[str(i)] = word_and_choices['correct']
        else:
            wrong_answer = random.choice(wrong_choices)
            wrong_choices.remove(wrong_answer)
            choice_assignments[str(i)] = wrong_answer
    choice_assignments['correct'] = str(correct_ans)
    choice_assignments['word'] = word_and_choices['word']
    return choice_assignments


def display_question(word_and_numerical_choices: dict[str, str]) -> None:
    print('Give the translation for:')
    print(word_and_numerical_choices['word'])
    for k in ['1', '2', '3', '4']:
        print(f'{k}: {word_and_numerical_choices[k]}')


def new_question(lines: list[str], from_english: bool = False) -> None:
    word_and_choices = pick_word_and_ans_choices(lines, from_english)
    word_and_num_choices = assign_choices(word_and_choices)
    display_question(word_and_num_choices)
    while True:
        player_input = input()
        if player_input.strip() == word_and_num_choices['correct']:
            print('Correct!')
            break
        elif player_input.strip() in ('1', '2', '3', '4'):
            print(f'Sorry, the correct answer is "{word_and_choices["correct"]}"')
            break
        else:
            print('Unrecognized input. Please input 1, 2, 3, or 4.')
