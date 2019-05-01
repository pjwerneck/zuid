
import mock

from zuid import ZUID


@mock.patch('os.urandom')
def test_generate_16_bytes_fixed_value(urandom_mock):
    # test with a fixed value of 1 to guarantee endianness and
    # justification is preserved between Python versions
    urandom_mock.return_value = bytearray([1])

    gen = ZUID(bytelength=16)

    assert gen.length == 22

    assert gen() == '0000000000000000000001'


def test_generate_16_bytes_no_prefix():

    gen = ZUID(bytelength=16)

    assert gen.length == 22

    ids = {gen() for x in range(1000)}

    assert len(ids) == 1000
    assert all(len(id_) == 22 for id_ in ids)


def test_generate_16_bytes_with_prefix():
    gen = ZUID(bytelength=16, prefix='test_')

    assert gen.length == 27

    ids = {gen() for x in range(1000)}

    assert len(ids) == 1000
    assert all(len(id_) == 27 for id_ in ids)
    assert all(id_.startswith('test_') for id_ in ids)


def test_generate_16_bytes_timestamped():
    gen = ZUID(bytelength=16, timestamped=True)

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


def test_generate_16_bytes_timestamped_order():
    gen = ZUID(bytelength=16, timestamped=True)

    assert gen.length == 22
    # test if ids stay in order when sorted
    ids = [gen() for x in range(1000)]

    assert sorted(ids) == ids


def test_generate_16_bytes_nontimestamped_order():
    gen = ZUID(bytelength=16, timestamped=False)

    assert gen.length == 22
    # test if ids stay in order when sorted
    ids = [gen() for x in range(1000)]

    assert sorted(ids) != ids
