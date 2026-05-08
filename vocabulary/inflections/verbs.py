import os
from vocabulary import VOCABULARY_FOLDER
import json
from utils.functions import render

PRESENT_SYSTEM_PERSONAL_ENDINGS = {
    'first': {
        'sg': '/o',
        'pl': 'mus'
    },
    'second': {
        'sg': 's',
        'pl': 'tis'
    },
    'third': {
        'sg': 't',
        'pl': 'nt'
    }
}


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
        return 'irregular'


def shorten_stem_vowel(verb_stem: str) -> str:
    if verb_stem.endswith('/a') or verb_stem.endswith('/e') or verb_stem.endswith('/i'):
        return ''.join(verb_stem.rsplit('/', maxsplit=1))
    else:
        raise ValueError(f"Verb stem {render(verb_stem)} not ending in {render('/a')}, {render('/e')}, or {render('/i')}.")


def validate_present_system(**kwargs) -> None:
    tense = kwargs.get('tense')
    if tense not in ('present', 'imperfect', 'future'):
        raise ValueError('Tense not in present system.')
    voice = kwargs.get('voice')
    if voice and voice != 'active':
        raise ValueError('Active voice required.')
    mood = kwargs.get('mood')
    if mood not in ('indicative', 'imperative', 'infinitive'):
        raise ValueError(f'Indicative, imperative, or infinitive mood required.')
    if (mood == 'imperative' or mood == 'infinitive') and tense != 'present':
        raise ValueError('Only present tense supported for infinitive and imperative moods.')


def conjugate_first_or_second_conjugation_present_system_regular(present_stem: str, person: str, number: str, tense: str,
                                                                 mood: str) -> str:
    validate_present_system(tense=tense, mood=mood)
    if mood == 'imperative' and person != 'second':
        raise ValueError('Imperative must be in second person.')
    conjugation = 'first' if present_stem.endswith('/a') else 'second'
    stem_to_use = present_stem
    if mood == 'infinitive':
        return stem_to_use + 're'
    elif mood == 'imperative':
        return stem_to_use if number == 'sg' else stem_to_use + 'te'
    if conjugation == 'first' and person == 'first' and number == 'sg' and tense == 'present':
        stem_to_use = stem_to_use[:-2]
    elif tense == 'present':
        if person == 'third':
            stem_to_use = shorten_stem_vowel(stem_to_use)
        elif person == 'first' and number == 'sg':
            stem_to_use = shorten_stem_vowel(stem_to_use)
    if tense == 'imperfect' and person == 'first' and number == 'sg':
        personal_ending = 'am'
    else:
        personal_ending = PRESENT_SYSTEM_PERSONAL_ENDINGS[person][number]
    if tense == 'present':
        return stem_to_use + personal_ending
    else:
        if person == 'first' and number == 'sg':
            tense_sign = 'b'
        elif tense == 'imperfect':
            tense_sign = 'ba'
        else:
            tense_sign = 'bi'
        if tense_sign == 'ba':
            if person == 'second':
                tense_sign = 'b/a'
            elif person == 'first' and number == 'pl':
                tense_sign = 'b/a'
        elif tense_sign == 'bi':
            if person == 'third' and number == 'pl':
                tense_sign = 'bu'
        return stem_to_use + tense_sign + personal_ending


def conjugate_third_conjugation_non_io_present_system_regular(present_stem: str, person: str, number: str, tense: str,
                                                              mood: str) -> str:
    validate_present_system(tense=tense, mood=mood)
    if mood == 'imperative' and person != 'second':
        raise ValueError('Imperative must be in second person.')
    if mood == 'infinitive':
        return present_stem + 're'
    if mood == 'imperative':
        return present_stem if number == 'sg' else present_stem[:-1] + 'ite'
    if person == 'first' and (tense == 'future' or tense == 'imperfect') and number == 'sg':
        personal_ending = 'am'
    else:
        personal_ending = PRESENT_SYSTEM_PERSONAL_ENDINGS[person][number]
    stem_to_use = present_stem[:-1]
    if tense == 'present':
        if not (person == 'first' and number == 'sg'):
            stem_to_use += 'i' if not (person == 'third' and number == 'pl') else 'u'
    elif tense == 'future':
        if not (person == 'first' and number == 'sg'):
            stem_to_use = present_stem if person == 'third' else stem_to_use + '/e'
    elif tense == 'imperfect':
        stem_to_use += '/e'
    if tense == 'present' or tense == 'future':
        return stem_to_use + personal_ending
    else:
        tense_sign = 'ba' if not (person == 'first' and number == 'sg') else 'b'
        if person == 'second' or (person == 'first' and number == 'pl'):
            tense_sign = 'b/a'
        return stem_to_use + tense_sign + personal_ending

