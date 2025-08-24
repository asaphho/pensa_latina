import json
import os
from nouns_adjs import NOUNS_FOLDER
import random


def capitalize(word: str) -> str:
    return word.replace(word[0], word[0].upper(), 1)


def is_capitalized(word: str) -> bool:
    return word[0].upper() == word[0]


def add_noun(json_filename: str, english: str, forms: list[str]) -> None:
    json_filepath = os.path.join(NOUNS_FOLDER, json_filename)
    file_exists = os.path.exists(json_filepath)
    noun_forms = list(set(forms))
    if not file_exists:
        nouns_data = {english: noun_forms}
        with open(json_filepath, 'w') as w:
            w.write(json.dumps(nouns_data, indent=4))
    else:
        with open(json_filepath, 'r') as f:
            nouns_data = json.load(f)
        nouns_data[english] = noun_forms
        with open(json_filepath, 'w') as w:
            w.write(json.dumps(nouns_data, indent=4))


def add_form(json_filename: str, english: str, form: str) -> None:
    json_filepath = os.path.join(NOUNS_FOLDER, json_filename)
    with open(json_filepath, 'r') as f:
        nouns_data = json.load(f)
    if english not in nouns_data:
        raise ValueError(f'{english} not found in nouns data')
    else:
        forms = nouns_data[english]
        new_forms = list(set(forms + [form]))
        nouns_data[english] = new_forms
        with open(json_filepath, 'w') as w:
            w.write(json.dumps(nouns_data, indent=4))


def get_wrong_form(nouns_data: dict[str, list[str]], english: str, correct_form: str) -> str:
    available_forms = [word for word in nouns_data[english] if word.lower() != correct_form.lower()]
    wrong_form = random.choice(available_forms)
    return capitalize(wrong_form) if is_capitalized(correct_form) else wrong_form


