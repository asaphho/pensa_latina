import os
from vocabulary import VOCABULARY_FOLDER
import json
from utils.functions import render


with open(os.path.join(VOCABULARY_FOLDER, 'inflection_data', 'verbs.json'), 'r') as f:
    VERBS_DATA = json.load(f)


def get_conjugation(verb_data: dict) -> str:
    principal_parts: list[str] = verb_data.get('principal_parts')
    if not principal_parts:
        raise ValueError('Principal parts not found.')
    infinitive = principal_parts[1]
    verb_stem = infinitive[:-2]
    if verb_stem.endswith('/a'):
        return 'first'
    elif verb_stem.endswith('e'):
        return 'second' if verb_stem.endswith('/e') else 'third'
    elif verb_stem.endswith('/i'):
        return 'fourth'
    else:
        raise ValueError(f'Unrecognized infinitive form {render(infinitive)}. Could not infer conjugation.')


def shorten_stem_vowel(verb_stem: str) -> str:
    if verb_stem.endswith('/a') or verb_stem.endswith('/e') or verb_stem.endswith('/i'):
        return ''.join(verb_stem.rsplit('/', maxsplit=1))
    else:
        raise ValueError(f"Verb stem {render(verb_stem)} not ending in {render('/a')}, {render('/e')}, or {render('/i')}.")
