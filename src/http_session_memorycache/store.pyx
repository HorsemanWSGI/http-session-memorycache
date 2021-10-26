import time
import typing as t
from threading import RLock
from http_session.meta import Store
from cromlech.marshallers import Marshaller, PickleMarshaller


MISSING = object()


cdef class Node:

    cdef readonly str key
    cdef readonly object value
    cdef public int timestamp
    cdef object __weakref__

    def __cinit__(self, str key, object value, int timestamp):
        self.key = key
        self.timestamp = timestamp
        self.value = value


cdef class MemoryStore:

    cdef readonly int TTL
    cdef readonly object serializer
    cdef dict _store
    cdef object _lock

    def __cinit__(self,
                  ttl: int = 300,
                  serializer: t.Optional[Marshaller] = PickleMarshaller):
        self.TTL = ttl
        self._store: t.Dict[str, Node] = {}
        self._lock = RLock()
        self.serializer = serializer

    def __len__(self):
        return len(self._store)

    cdef _has_expired(self, value):
        return self.TTL and (value.timestamp + self.TTL) < time.time()

    cpdef Node get_node(self, key: str):
        with self._lock:
            node = self._store.get(key, MISSING)
            if node is MISSING:
                raise KeyError(key)
            if self._has_expired(node):
                self.delete(key)
                raise KeyError(key)
        return node

    cpdef get(self, key: str):
        node = self.get_node(key)
        node.timestamp = time.time()
        if self.serializer is not None:
            return self.serializer.loads(node.value)
        return node.value

    cpdef set(self, key: str, value: t.Any):
        with self._lock:
            if not isinstance(value, Node):
                if self.serializer is not None:
                    value = self.serializer.dumps(value)
                value = Node(
                    key=key,
                    value=value,
                    timestamp=time.time()
                )
            self._store[key] = value

    cpdef delete(self, key: str):
        with self._lock:
            del self._store[key]

    cpdef clear(self):
        with self._lock:
            self._store.clear()

    cpdef flush_expired(self):
        with self._lock:
            expired = {
                value.key for value in self._store.values()
                if self._has_expired(value)
            }
            for key in expired:
                self.delete(key)

    cpdef touch(self, key: str):
        with self._lock:
            node = self.get_node(key)
            node.timestamp = time.time()


Store.register(MemoryStore)
