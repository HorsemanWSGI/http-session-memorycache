import pytest
from datetime import datetime
from http_session_memorycache.store import MemoryStore
from freezegun import freeze_time


def test_store():
    store = MemoryStore(300)
    store.set('test', {'this': 'is a session'})
    assert store.get('test') == {'this': 'is a session'}
    with pytest.raises(KeyError):
        store.get('nothing')


def test_timeout():
    store = MemoryStore(300)

    with freeze_time('2021-10-22 21:00:00'):
        store.set('test', {'this': 'is a session'})
        assert store.get('test') == {'this': 'is a session'}

    with freeze_time('2021-10-22 21:05:01'):
        with pytest.raises(KeyError):
            store.get('test')


def test_touch():
    store = MemoryStore(300)

    with freeze_time('2021-10-22 21:00:00'):
        store.set('test', {'this': 'is a session'})
        assert store.get('test') == {'this': 'is a session'}
        assert len(store) == 1
        node = store.get_node('test')
        assert node.timestamp == 1634936400

    with freeze_time('2021-10-22 21:04:00'):
        store.touch('test')
        assert len(store) == 1
        node = store.get_node('test')
        assert node.timestamp == 1634936640

    with freeze_time('2021-10-22 21:05:01'):
        assert store.get('test') == {'this': 'is a session'}

    with freeze_time('2021-10-22 21:09:01'):
        assert store.get('test') == {'this': 'is a session'}


def test_flush():
    store = MemoryStore(300)

    with freeze_time('2021-10-22 21:00:00'):
        store.set('test', {'this': 'is a session'})

    with freeze_time('2021-10-22 21:01:00'):
        store.set('another test', {'this': 'is another session'})

    with freeze_time('2021-10-22 21:01:30'):
        store.set('foo', {'bar': 'qux'})
        assert len(store) == 3

    with freeze_time('2021-10-22 21:06:01'):
        store.flush_expired()
        assert len(store) == 1
        assert store.get('foo') == {'bar': 'qux'}
