from typing import NamedTuple, Any, List, Optional, Union


class Pair(NamedTuple):
    key: Any
    value: Any


class Deleted:
    pass


class HashTable:
    DELETED = Deleted

    def __init__(self, capacity: int = 4):
        self.capacity = capacity
        self._array: List[Optional[Union[Pair, Deleted]]] = [None] * self.capacity

    @property
    def capacity(self):
        return self.__capacity

    @capacity.setter
    def capacity(self, value):
        if value < 1:
            raise ValueError("Capacity must be positive number")
        self.__capacity = value

    @property
    def array(self):
        return {pair for pair in self._array if pair not in (None, self.DELETED)}

    @property
    def keys(self):
        return {pair.key for pair in self.array}

    @property
    def values(self):
        return {pair.value for pair in self.array}

    def hash(self, key):
        # return sum(ord(char) for char in key) % self.capacity
        return hash(key) % self.capacity

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __len__(self):
        return len(self.array)

    def __setitem__(self, key, value):
        for index, pair in self._probe(key):
            if pair is self.DELETED:
                continue
            if pair is None or pair.key == key:
                self._array[index] = Pair(key, value)
                break
        else:
            self._resize()
            self.key = value

    def __getitem__(self, key):
        for _, pair in self._probe(key):
            if pair is self.DELETED:
                continue
            if pair is None:
                raise KeyError(key)
            if pair.key == key:
                return pair.value
        else:
            KeyError(key)

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def __delitem__(self, key):
        for index, pair in self._probe(key):
            if pair is self.DELETED:
                continue
            if pair is None:
                raise KeyError(key)
            if pair.key == key:
                self._array[index] = self.DELETED
                break
        else:
            raise KeyError(key)

    def __iter__(self):
        yield from self.keys

    def __str__(self):
        pairs = []
        for key, value in self.array:
            pairs.append(f"{key!r} {value!r}")
            return "{" + ", ".join(pairs) + "}"

    def _probe(self, key):
        index = self.hash(key)
        for _ in range(self.capacity):
            yield index, self._array[index]
            index = (index + 1) % self.capacity

    def _resize(self):
        copy = HashTable(capacity=self.capacity * 2)
        for key, value in self.array:
            copy[key] = value
        self.capacity = copy.capacity
        self._array = copy._array


# Test code:
table = HashTable()
table["name"] = "Peter"
table["age"] = 25
table["city"] = "Sofia"
table["job"] = "programmer"

print(table)
print(table.get("name"))
print(table["age"])
print(len(table))

print("age" in table)

