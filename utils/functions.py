import json
import os
from decl_conj import DECL_CONJ_FOLDER
import random

DIPHTHONGS = ('ae', 'au', 'ei', 'eu', 'oe', 'ui')

VOWELS = ('a', 'e', 'i', 'o', 'u', 'y')


def capitalize(word: str) -> str:
    return word.replace(word[0], word[0].upper(), 1)


def is_capitalized(word: str) -> bool:
    return word[0].upper() == word[0]


def add_word(json_filename: str, english: str, forms: list[str]) -> None:
    json_filepath = os.path.join(DECL_CONJ_FOLDER, json_filename)
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
    json_filepath = os.path.join(DECL_CONJ_FOLDER, json_filename)
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


_MACRONS = {
    '/a': 'ā', '/A': 'Ā',
    '/e': 'ē', '/E': 'Ē',
    '/i': 'ī', '/I': 'Ī',
    '/o': 'ō', '/O': 'Ō',
    '/u': 'ū', '/U': 'Ū',
}


def render(text: str) -> str:
    for code, macron in _MACRONS.items():
        text = text.replace(code, macron)
    return text


def get_wrong_form(nouns_data: dict[str, list[str]], english: str, correct_form: str) -> str:
    available_forms = [word for word in nouns_data[english] if word.lower() != correct_form.lower()]
    wrong_form = random.choice(available_forms)
    return capitalize(wrong_form) if is_capitalized(correct_form) else wrong_form


def compare_spellings(generated_word: str, input_word: str) -> bool:
    return generated_word.replace('/', '').lower() == input_word.strip().lower()


def is_consonantal_i(word_with_slashes: str, index: int) -> bool:
    if word_with_slashes.lower().replace('/', '') == 'ii':
        return False
    next_index = index + 1
    if next_index >= len(word_with_slashes):
        return False
    if index == 0:
        next_character = word_with_slashes.lower()[1]
        return (next_character == '/') or (next_character in VOWELS)
    else:
        prev_index = index - 1
        prev_character = word_with_slashes.lower()[prev_index]
        if prev_character == '/':
            return False
        else:
            if prev_character not in VOWELS:
                return False
            else:
                next_character = word_with_slashes.lower()[next_index]
                return (next_character == '/') or next_character in VOWELS


def i_part_of_diphthong(word_with_slashes: str, index: int) -> bool:
    if index == 0:
        return False
    else:
        prev_index = index - 1
        if prev_index == 0:
            return word_with_slashes[:2].lower() in DIPHTHONGS
        else:
            prev_prev_index = prev_index - 1
            if word_with_slashes[prev_prev_index] == '/':
                return False
            else:
                return word_with_slashes[prev_index:index + 1].lower() in DIPHTHONGS


def qu_must_be_counted(word_with_slashes: str, index: int) -> bool:
    next_character = word_with_slashes.lower()[index + 2]
    if next_character == '/':
        return True
    else:
        return word_with_slashes.lower()[index + 1:index + 3] not in DIPHTHONGS


def count_syllables(word_with_slashes: str) -> int:
    false_diphthongs = [f'/{d}' for d in DIPHTHONGS]
    word = word_with_slashes.lower()
    total_vowels = sum([word.count(v) for v in VOWELS])
    total_diphthongs = sum([word.count(d) for d in DIPHTHONGS])
    compensate_for_false = sum([word.count(f) for f in false_diphthongs])
    i_indices = [i for i in range(len(word)) if word[i] == 'i']
    consonantal_i_indices = [i for i in i_indices if is_consonantal_i(word_with_slashes, i)]
    consonantal_i_in_diphthongs = [i for i in consonantal_i_indices if i_part_of_diphthong(word_with_slashes, i)]
    qu_indices = [i for i in range(len(word)) if word[i] == 'q']
    compensate_for_consonantal_u = sum([int(qu_must_be_counted(word_with_slashes, i)) for i in qu_indices])
    return total_vowels - total_diphthongs + compensate_for_false - len(consonantal_i_indices) \
           + len(consonantal_i_in_diphthongs) - compensate_for_consonantal_u
