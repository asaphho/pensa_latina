import vocabulary.inflections.nouns as nouns
import json
import os
from vocabulary import VOCABULARY_FOLDER

with open(os.path.join(VOCABULARY_FOLDER, 'inflection_data', 'nouns.json'), 'r') as f:
    NOUNS_DATA = json.load(f)


def test_get_declension():
    defective_data = NOUNS_DATA.get('n/em/o')
    assert nouns.get_declension(defective_data) == 'defective'
    indeclinable_data = NOUNS_DATA.get('nihil')
    assert nouns.get_declension(indeclinable_data) == 'indeclinable'
    data1 = NOUNS_DATA.get('f/ilia')
    assert nouns.get_declension(data1) == 'first'
    data1a = NOUNS_DATA.get('/insidiae')
    assert nouns.get_declension(data1a) == 'first'
    data2 = NOUNS_DATA.get('filius')
    assert nouns.get_declension(data2) == 'second'
    data3 = NOUNS_DATA.get('adul/esc/ens')
    assert nouns.get_declension(data3) == 'third'


def test_decline_defective():
    defective_data = NOUNS_DATA.get('n/em/o')
    expected_forms = {'nom': 'n/em/o', 'gen': 'null/ius', 'dat': 'n/emin/i', 'acc': 'n/eminem', 'abl': 'n/ull/o',
                      'voc': 'n/em/o'}
    for case in expected_forms:
        assert nouns.decline_defective_noun(defective_data, case, 'sg') == expected_forms[case]


def test_decline_irregular():
    assert nouns.decline_noun('f/ilia', 'dat', 'pl') == 'f/ili/abus'
    assert nouns.decline_noun('f/ilia', 'abl', 'pl') == 'f/ili/abus'


def test_decline_first_declension_regular():
    assert nouns.decline_first_declension_regular('po/etae', 'nom', 'sg', False) == 'po/eta'
    assert nouns.decline_first_declension_regular('po/etae', 'gen', 'sg', False) == 'po/etae'
    assert nouns.decline_first_declension_regular('po/etae', 'dat', 'sg', False) == 'po/etae'
    assert nouns.decline_first_declension_regular('po/etae', 'acc', 'sg', False) == 'po/etam'
    assert nouns.decline_first_declension_regular('po/etae', 'abl', 'sg', False) == 'po/et/a'
    assert nouns.decline_first_declension_regular('po/etae', 'voc', 'sg', False) == 'po/eta'
    assert nouns.decline_first_declension_regular('po/etae', 'nom', 'pl', False) == 'po/etae'
    assert nouns.decline_first_declension_regular('po/etae', 'gen', 'pl', False) == 'po/et/arum'
    assert nouns.decline_first_declension_regular('po/etae', 'dat', 'pl', False) == 'po/et/is'
    assert nouns.decline_first_declension_regular('po/etae', 'acc', 'pl', False) == 'po/et/as'
    assert nouns.decline_first_declension_regular('po/etae', 'abl', 'pl', False) == 'po/et/is'
    assert nouns.decline_first_declension_regular('po/etae', 'voc', 'pl', False) == 'po/etae'


def test_decline_first_declension_regular_plural_only():
    assert nouns.decline_first_declension_regular('/insidi/arum', 'nom', 'pl', True) == '/insidiae'
    assert nouns.decline_first_declension_regular('/insidi/arum', 'gen', 'pl', True) == '/insidi/arum'
    assert nouns.decline_first_declension_regular('/insidi/arum', 'dat', 'pl', True) == '/insidi/is'
    assert nouns.decline_first_declension_regular('/insidi/arum', 'acc', 'pl', True) == '/insidi/as'
    assert nouns.decline_first_declension_regular('/insidi/arum', 'abl', 'pl', True) == '/insidi/is'
    assert nouns.decline_first_declension_regular('/insidi/arum', 'voc', 'pl', True) == '/insidiae'


def test_decline_second_declension_us_regular():
    assert nouns.decline_second_declension_regular('am/icus', 'am/ic/i', 'm', 'nom', 'sg', False) == 'am/icus'
    assert nouns.decline_second_declension_regular('am/icus', 'am/ic/i', 'm', 'gen', 'sg', False) == 'am/ic/i'
    assert nouns.decline_second_declension_regular('am/icus', 'am/ic/i', 'm', 'dat', 'sg', False) == 'am/ic/o'
    assert nouns.decline_second_declension_regular('am/icus', 'am/ic/i', 'm', 'acc', 'sg', False) == 'am/icum'
    assert nouns.decline_second_declension_regular('am/icus', 'am/ic/i', 'm', 'abl', 'sg', False) == 'am/ic/o'
    assert nouns.decline_second_declension_regular('am/icus', 'am/ic/i', 'm', 'voc', 'sg', False) == 'am/ice'
