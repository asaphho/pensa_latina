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


