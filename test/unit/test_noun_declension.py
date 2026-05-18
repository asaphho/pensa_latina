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
    assert nouns.decline_second_declension_regular('am/icus', 'am/ic/i', 'm', 'nom', 'pl', False) == 'am/ic/i'
    assert nouns.decline_second_declension_regular('am/icus', 'am/ic/i', 'm', 'gen', 'pl', False) == 'am/ic/orum'
    assert nouns.decline_second_declension_regular('am/icus', 'am/ic/i', 'm', 'dat', 'pl', False) == 'am/ic/is'
    assert nouns.decline_second_declension_regular('am/icus', 'am/ic/i', 'm', 'acc', 'pl', False) == 'am/ic/os'
    assert nouns.decline_second_declension_regular('am/icus', 'am/ic/i', 'm', 'abl', 'pl', False) == 'am/ic/is'
    assert nouns.decline_second_declension_regular('am/icus', 'am/ic/i', 'm', 'voc', 'pl', False) == 'am/ic/i'


def test_decline_second_declension_ius_vocative():
    assert nouns.decline_second_declension_regular('filius', 'fili/i', 'm', 'voc', 'sg', False) == 'fil/i'


def test_decline_second_declension_non_us_regular():
    assert nouns.decline_second_declension_regular('puer', 'puer/i', 'm', 'voc', 'sg', False) == 'puer'
    assert nouns.decline_second_declension_regular('ager', 'agr/i', 'm', 'dat', 'sg', False) == 'agr/o'


def test_decline_third_declension_non_i_stem_non_neuter():
    assert nouns.decline_third_declension_regular('amor', 'am/oris', 'm', 'nom', 'sg', False) == 'amor'
    assert nouns.decline_third_declension_regular('amor', 'am/oris', 'm', 'gen', 'sg', False) == 'am/oris'
    assert nouns.decline_third_declension_regular('amor', 'am/oris', 'm', 'dat', 'sg', False) == 'am/or/i'
    assert nouns.decline_third_declension_regular('amor', 'am/oris', 'm', 'acc', 'sg', False) == 'am/orem'
    assert nouns.decline_third_declension_regular('amor', 'am/oris', 'm', 'abl', 'sg', False) == 'am/ore'
    assert nouns.decline_third_declension_regular('amor', 'am/oris', 'm', 'voc', 'sg', False) == 'amor'
    assert nouns.decline_third_declension_regular('amor', 'am/oris', 'm', 'nom', 'pl', False) == 'am/or/es'
    assert nouns.decline_third_declension_regular('amor', 'am/oris', 'm', 'gen', 'pl', False) == 'am/orum'
    assert nouns.decline_third_declension_regular('amor', 'am/oris', 'm', 'dat', 'pl', False) == 'am/oribus'
    assert nouns.decline_third_declension_regular('amor', 'am/oris', 'm', 'acc', 'pl', False) == 'am/or/es'
    assert nouns.decline_third_declension_regular('amor', 'am/oris', 'm', 'abl', 'pl', False) == 'am/oribus'
    assert nouns.decline_third_declension_regular('amor', 'am/oris', 'm', 'voc', 'pl', False) == 'am/or/es'


def test_decline_third_declension_non_i_stem_neuter():
    assert nouns.decline_third_declension_regular('corpus', 'corporis', 'n', 'acc', 'sg', False) == 'corpus'
    assert nouns.decline_third_declension_regular('corpus', 'corporis', 'n', 'nom', 'pl', False) == 'corpora'
    assert nouns.decline_third_declension_regular('corpus', 'corporis', 'n', 'acc', 'pl', False) == 'corpora'


def test_decline_third_declension_i_stem_rule1():
    assert nouns.decline_third_declension_regular('n/ub/es', 'n/ubis', 'f', 'nom', 'sg', False) == 'n/ub/es'
    assert nouns.decline_third_declension_regular('n/ub/es', 'n/ubis', 'f', 'gen', 'sg', False) == 'n/ubis'
    assert nouns.decline_third_declension_regular('n/ub/es', 'n/ubis', 'f', 'dat', 'sg', False) == 'n/ub/i'
    assert nouns.decline_third_declension_regular('n/ub/es', 'n/ubis', 'f', 'acc', 'sg', False) == 'n/ubem'
    assert nouns.decline_third_declension_regular('n/ub/es', 'n/ubis', 'f', 'abl', 'sg', False) == 'n/ube'
    assert nouns.decline_third_declension_regular('n/ub/es', 'n/ubis', 'f', 'voc', 'sg', False) == 'n/ub/es'
    assert nouns.decline_third_declension_regular('n/ub/es', 'n/ubis', 'f', 'nom', 'pl', False) == 'n/ub/es'
    assert nouns.decline_third_declension_regular('n/ub/es', 'n/ubis', 'f', 'gen', 'pl', False) == 'n/ubium'
    assert nouns.decline_third_declension_regular('n/ub/es', 'n/ubis', 'f', 'dat', 'pl', False) == 'n/ubibus'
    assert nouns.decline_third_declension_regular('n/ub/es', 'n/ubis', 'f', 'acc', 'pl', False) == 'n/ub/es'
    assert nouns.decline_third_declension_regular('n/ub/es', 'n/ubis', 'f', 'abl', 'pl', False) == 'n/ubibus'
    assert nouns.decline_third_declension_regular('n/ub/es', 'n/ubis', 'f', 'voc', 'pl', False) == 'n/ub/es'


def test_decline_third_declension_i_stem_rule2():
    assert nouns.decline_third_declension_regular('ars', 'artis', 'f', 'nom', 'sg', False) == 'ars'
    assert nouns.decline_third_declension_regular('ars', 'artis', 'f', 'gen', 'sg', False) == 'artis'
    assert nouns.decline_third_declension_regular('ars', 'artis', 'f', 'dat', 'sg', False) == 'art/i'
    assert nouns.decline_third_declension_regular('ars', 'artis', 'f', 'acc', 'sg', False) == 'artem'
    assert nouns.decline_third_declension_regular('ars', 'artis', 'f', 'abl', 'sg', False) == 'arte'
    assert nouns.decline_third_declension_regular('ars', 'artis', 'f', 'voc', 'sg', False) == 'ars'
    assert nouns.decline_third_declension_regular('ars', 'artis', 'f', 'nom', 'pl', False) == 'art/es'
    assert nouns.decline_third_declension_regular('ars', 'artis', 'f', 'gen', 'pl', False) == 'artium'
    assert nouns.decline_third_declension_regular('ars', 'artis', 'f', 'dat', 'pl', False) == 'artibus'
    assert nouns.decline_third_declension_regular('ars', 'artis', 'f', 'acc', 'pl', False) == 'art/es'
    assert nouns.decline_third_declension_regular('ars', 'artis', 'f', 'abl', 'pl', False) == 'artibus'
    assert nouns.decline_third_declension_regular('ars', 'artis', 'f', 'voc', 'pl', False) == 'art/es'


def test_decline_third_declension_i_stem_rule3():
    assert nouns.decline_third_declension_regular('mare', 'maris', 'n', 'nom', 'sg', False) == 'mare'
    assert nouns.decline_third_declension_regular('mare', 'maris', 'n', 'gen', 'sg', False) == 'maris'
    assert nouns.decline_third_declension_regular('mare', 'maris', 'n', 'dat', 'sg', False) == 'mar/i'
    assert nouns.decline_third_declension_regular('mare', 'maris', 'n', 'acc', 'sg', False) == 'mare'
    assert nouns.decline_third_declension_regular('mare', 'maris', 'n', 'abl', 'sg', False) == 'mar/i'
    assert nouns.decline_third_declension_regular('mare', 'maris', 'n', 'voc', 'sg', False) == 'mare'
    assert nouns.decline_third_declension_regular('mare', 'maris', 'n', 'nom', 'pl', False) == 'maria'
    assert nouns.decline_third_declension_regular('mare', 'maris', 'n', 'gen', 'pl', False) == 'marium'
    assert nouns.decline_third_declension_regular('mare', 'maris', 'n', 'dat', 'pl', False) == 'maribus'
    assert nouns.decline_third_declension_regular('mare', 'maris', 'n', 'acc', 'pl', False) == 'maria'
    assert nouns.decline_third_declension_regular('mare', 'maris', 'n', 'abl', 'pl', False) == 'maribus'
    assert nouns.decline_third_declension_regular('mare', 'maris', 'n', 'voc', 'pl', False) == 'maria'
