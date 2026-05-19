from vocabulary import VOCABULARY_FOLDER
import os
import json
from utils.functions import render, count_syllables, VOWELS

with open(os.path.join(VOCABULARY_FOLDER, 'inflection_data', 'nouns.json'), 'r') as f:
    NOUNS_DATA = json.load(f)


def get_declension(noun_data: dict) -> str:
    if noun_data.get('defective'):
        return 'defective'
    elif noun_data.get('indeclinable'):
        return 'indeclinable'
    else:
        genitive = noun_data.get('genitive')
        if not genitive:
            raise ValueError('Genitive form not found. Could not infer declension.')
        genitive_is_singular = bool(noun_data.get('plural_only')) is False
        if genitive_is_singular:
            if genitive.endswith('ae'):
                return 'first'
            elif genitive.endswith('/i'):
                return 'fifth' if genitive.endswith('e/i') else 'second'
            elif genitive.endswith('is'):
                return 'third'
            elif genitive.endswith('/us'):
                return 'fourth'
            else:
                raise ValueError(f'Unrecognized genitive form: {render(genitive)}.')
        else:
            if genitive.endswith('/arum'):
                return 'first'
            elif genitive.endswith('/orum'):
                return 'second'
            elif genitive.endswith('/erum'):
                return 'fifth'
            elif genitive.endswith('um'):
                return 'fourth' if genitive.endswith('uum') else 'third'
            else:
                raise ValueError(f'Unrecognized genitive form: {render(genitive)}.')


def decline_defective_noun(noun_data: dict, case: str, number: str) -> str:
    paradigm: dict[str, dict[str, str]] = noun_data.get('paradigm')
    if not paradigm:
        raise ValueError('Paradigm not found in noun data.')
    endings_for_number = paradigm.get(number)
    if not endings_for_number:
        raise ValueError('Form does not exist.')
    form = endings_for_number.get(case)
    if not form:
        raise ValueError('Form does not exist.')
    else:
        return form


def decline_first_declension_regular(genitive: str, case: str, number: str, plural_only: bool) -> str:
    stem = genitive[:-5] if plural_only else genitive[:-2]
    if number == 'sg' and plural_only:
        raise ValueError('No singular form exists.')
    if number == 'sg':
        if case == 'nom' or case == 'voc':
            return stem + 'a'
        elif case == 'gen' or case == 'dat':
            return genitive
        elif case == 'abl':
            return stem + '/a'
        else:
            return stem + 'am'
    else:
        if case == 'nom' or case == 'voc':
            return stem + 'ae'
        elif case == 'gen':
            return stem + '/arum'
        elif case == 'dat' or case == 'abl':
            return stem + '/is'
        else:
            return stem + '/as'


def decline_second_declension_regular(nominative: str, genitive: str, gender: str, case: str, number: str,
                                      plural_only: bool) -> str:
    stem = genitive[:-5] if plural_only else genitive[:-2]
    if number == 'sg' and plural_only:
        raise ValueError('No singular form exists.')
    if number == 'sg':
        if case == 'nom':
            return nominative
        elif case == 'gen':
            return genitive
        elif case == 'dat' or case == 'abl':
            return stem + '/o'
        elif case == 'acc':
            return nominative if gender == 'n' else stem + 'um'
        else:
            if not nominative.endswith('us'):
                return nominative
            elif nominative.endswith('ius'):
                return nominative[:-3] + '/i'
            else:
                return stem + 'e'
    else:
        if case == 'nom' or case == 'voc':
            return stem + 'a' if gender == 'n' else stem + '/i'
        elif case == 'gen':
            return stem + '/orum'
        elif case == 'dat' or case == 'abl':
            return stem + '/is'
        else:
            return stem + 'a' if gender == 'n' else stem + '/os'


def decline_third_declension_regular(nominative: str, genitive: str, gender: str, case: str, number: str,
                                     plural_only: bool) -> str:
    stem = genitive[:-2]
    if plural_only:
        i_stem = False
    else:
        if gender != 'n':
            if nominative.endswith('es') or nominative.endswith('is'):
                i_stem = count_syllables(nominative) == count_syllables(genitive)
            elif nominative.endswith('s') or nominative.endswith('x'):
                last_two_of_stem = stem[-2:].lower()
                i_stem = (len(last_two_of_stem) == 2) and (not any([letter in VOWELS for letter in last_two_of_stem]))
            else:
                i_stem = False
        else:
            i_stem = nominative.endswith('al') or nominative.endswith('ar') or nominative.endswith('e')
    if number == 'sg' and plural_only:
        raise ValueError('No singular form exists.')
    if number == 'sg':
        if case == 'nom' or case == 'voc':
            return nominative
        elif case == 'gen':
            return genitive
        elif case == 'dat':
            return stem + '/i'
        elif case == 'acc':
            return nominative if gender == 'n' else stem + 'em'
        else:
            return stem + 'e' if not ((gender == 'n') and i_stem) else stem + '/i'
    else:
        if case in ('nom', 'acc', 'voc'):
            if not i_stem:
                return stem + 'a' if gender == 'n' else stem + '/es'
            else:
                return stem + 'ia' if gender == 'n' else stem + '/es'
        elif case == 'gen':
            return stem + 'um' if not i_stem else stem + 'ium'
        else:
            return stem + 'ibus'


def decline_noun(nominative: str, case: str, number: str) -> str:
    noun_data: dict = NOUNS_DATA.get(nominative)
    if not noun_data:
        raise ValueError(f'Noun data for {render(nominative)} not found!')
    declension = get_declension(noun_data)
    if declension == 'defective':
        return decline_defective_noun(noun_data=noun_data, case=case, number=number)
    elif declension == 'indeclinable':
        return nominative
    else:
        irregularities: list[dict[str, str]] = noun_data.get('irregularities')
        if irregularities:
            matching = [case_form for case_form in irregularities if case_form.get('case') == case
                        and case_form.get('number') == number]
            if matching:
                return matching[0].get('form')
        plural_only = bool(noun_data.get('plural_only'))
        gender: str = noun_data.get('gender')
        if gender not in ('m', 'f', 'n'):
            raise ValueError(f'Invalid or missing gender entry for {render(nominative)} in noun data.')
        genitive: str = noun_data.get('genitive')
        if not genitive:
            raise ValueError(f'Missing genitive entry for {render(nominative)} in noun data.')
        if declension == 'first':
            return decline_first_declension_regular(genitive=genitive, case=case, number=number,
                                                    plural_only=plural_only)
        elif declension == 'second':
            return decline_second_declension_regular(nominative=nominative, genitive=genitive, gender=gender, case=case,
                                                     number=number, plural_only=plural_only)
        elif declension == 'third':
            return decline_third_declension_regular(nominative=nominative, genitive=genitive, gender=gender, case=case,
                                                    number=number, plural_only=plural_only)
        else:
            raise NotImplementedError('Fourth and fifth declensions are not implemented yet.')

