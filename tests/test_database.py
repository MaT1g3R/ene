from itertools import chain
from sqlite3 import DatabaseError
from pathlib import Path

import pytest

from ene.database import Database
from . import HERE

MOCK_SQL = HERE / 'mock_db.sql'
MOCK_SHOWS = {
        'foo': [Path('foo episode 1'),
                Path('foo episode 2'),
                Path('foo episode 3'),
                Path('foo episode 4'),
                Path('foo episode 5')],
        'bar': [Path('bar episode 1'),
                Path('bar episode 2'),
                Path('bar episode 3')],
        'baz': [Path('baz episode 1'),
                Path('baz episode 2'),
                Path('baz episode 3'),
                Path('baz episode 4')]
    }


@pytest.fixture
def empty_db() -> Database:
    db = Database(Path(':memory:'))
    db.initial_setup()
    yield db
    del db


@pytest.fixture
def mock_db() -> Database:
    db = Database(Path(':memory:'))
    db.initial_setup()
    db.cursor.executescript(MOCK_SQL.read_text())
    yield db
    del db


def test_get_shows(mock_db):
    assert list(MOCK_SHOWS.keys()) == mock_db.get_all_shows()


def test_get_show_by_name(mock_db):
    assert mock_db.get_show_id_by_name('foo') == 1
    assert mock_db.get_show_id_by_name('bar') == 2
    assert mock_db.get_show_id_by_name('baz') == 3


def test_get_nonexistent_show(mock_db):
    assert mock_db.get_show_id_by_name('quz') is None


def test_get_episodes_for_show(mock_db):
    for show in MOCK_SHOWS:
        assert mock_db.get_episodes_by_show_name(show) == MOCK_SHOWS[show]


def test_get_episodes_for_nonexistent_show(empty_db):
    assert None is empty_db.get_episodes_by_show_name('quz')


def test_get_all(mock_db):
    assert mock_db.get_all() == MOCK_SHOWS


def test_get_episodes(mock_db):
    assert mock_db.get_all_episodes() == list(chain.from_iterable(MOCK_SHOWS.values()))


def test_write_show(empty_db):
    assert empty_db.add_show('foo') == 1
    assert empty_db.get_show_id_by_name('foo') == 1


def test_write_episode(empty_db):
    assert empty_db.add_episode_by_show_name(Path('foo episode 1'), 'foo') == 1
    assert empty_db.get_show_id_by_name('foo') == 1
    assert empty_db.add_episode_by_show_name(Path('foo episode 2'), 'foo') == 2
    assert empty_db.get_episodes_by_show_name('foo') == [Path('foo episode 1'),
                                                         Path('foo episode 2')]


def test_write_all_episodes(empty_db):
    empty_db.add_show('foo')
    empty_db.write_all_episodes_delta(MOCK_SHOWS)
    assert MOCK_SHOWS == empty_db.get_all()


def test_write_all_shows(empty_db):
    empty_db.write_all_shows_delta(MOCK_SHOWS)
    assert sorted(list(MOCK_SHOWS.keys())) == empty_db.get_all_shows()


def test_write_all_shows_delta(empty_db):
    empty_db.add_show('foo')
    empty_db.write_all_shows_delta(MOCK_SHOWS)
    assert list(MOCK_SHOWS.keys()) == empty_db.get_all_shows()


def test_write_all_episodes_delta(empty_db):
    for key in MOCK_SHOWS:
        empty_db.add_episode_by_show_name(MOCK_SHOWS[key][0], key)
    empty_db.write_all_episodes_delta(MOCK_SHOWS)
    assert MOCK_SHOWS == empty_db.get_all()