
from zuid import ZUID

from freezegun import freeze_time


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
    with freeze_time('2019-05-01 0:00:00.000001'):
        ids = {gen() for x in range(1000)}

        print(ids)

        assert len(ids) == 1000
        assert all(len(id_) == 22 for id_ in ids)
        assert all(id_.startswith('1qzYhAtIv7A') for id_ in ids)

    with freeze_time('2019-05-01 0:00:00.000002'):
        ids = {gen() for x in range(1000)}

        print(ids)

        assert len(ids) == 1000
        assert all(len(id_) == 22 for id_ in ids)
        assert all(id_.startswith('1qzYhAtIvJY') for id_ in ids)


def test_generate_16_bytes_timestamped_order():
    gen = ZUID(bytelength=16, timestamped=True)

    assert gen.length == 22
    # test if ids stay in order when sorted
    ids = [gen() for x in range(1000)]

    assert sorted(ids) == ids
