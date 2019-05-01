
import mock

from zuid import ZUID


@mock.patch('random.SystemRandom.choice')
def test_generate_22_chars_fixed_value(choice_mock):
    choice_mock.return_value = '0'

    gen = ZUID(length=22)

    assert gen.length == 22

    assert gen() == '0' * 22


def test_generate_22_chars_no_prefix():

    gen = ZUID(length=22)

    assert gen.length == 22

    ids = {gen() for x in range(1000)}

    assert len(ids) == 1000
    assert all(len(id_) == 22 for id_ in ids)


def test_generate_22_chars_with_prefix():
    gen = ZUID(length=22, prefix='test_')

    assert gen.length == 27

    ids = {gen() for x in range(1000)}

    assert len(ids) == 1000
    assert all(len(id_) == 27 for id_ in ids)
    assert all(id_.startswith('test_') for id_ in ids)


def test_generate_22_chars_timestamped():
    gen = ZUID(length=22, timestamped=True)

    assert gen.length == 22

    # test if first bytes change with time
    with mock.patch('time.time') as mock_time:
        mock_time.return_value = 1e-9
        ids = {gen() for x in range(1000)}

        assert len(ids) == 1000
        assert all(len(id_) == 22 for id_ in ids)
        assert all(id_.startswith('00000000001') for id_ in ids)

    with mock.patch('time.time') as mock_time:
        mock_time.return_value = 2e-9
        ids = {gen() for x in range(1000)}

        assert len(ids) == 1000
        assert all(len(id_) == 22 for id_ in ids)
        assert all(id_.startswith('00000000002') for id_ in ids)


def test_generate_22_chars_timestamped_order():
    gen = ZUID(length=22, timestamped=True)

    assert gen.length == 22
    # test if ids stay in order when sorted
    ids = [gen() for x in range(1000)]

    assert sorted(ids) == ids


def test_generate_22_chars_nontimestamped_order():
    gen = ZUID(length=22, timestamped=False)

    assert gen.length == 22
    # test if ids stay in order when sorted
    ids = [gen() for x in range(1000)]

    assert sorted(ids) != ids
