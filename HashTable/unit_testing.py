from itertools import permutations
from unittest import TestCase, main

from hash_table import HashTable


class TestHashTable(TestCase):
    def setUp(self) -> None:
        self.hash_table = HashTable(capacity=4)
        self.hash_table['hello'] = 'Hello World!'
        self.hash_table[98.6] = 37
        self.hash_table[False] = True

    def test_should_create_table(self):
        self.assertIsNotNone(self.hash_table)

    def test_len_of_empty_hash_table(self):
        self.assertEqual(0, len(HashTable(100)))

    def test_create_empty_pair_slots(self):
        hash_table = HashTable(4)

        expected = [None, None, None, None]
        actual = hash_table._array
        self.assertEqual(expected, actual)

    def test_should_insert_key_value_pairs(self):
        self.assertIn(('hello', 'Hello World!'), self.hash_table.array)
        self.assertIn((98.6, 37), self.hash_table.array)
        self.assertIn((False, True), self.hash_table.array)
        self.assertEqual(3, len(self.hash_table))

    def test_should_find_key(self):
        self.assertIn('hello', self.hash_table)
        self.assertIn(98.6, self.hash_table)
        self.assertIn(False, self.hash_table)

    def test_should_not_find_missing_key(self):
        self.assertNotIn("missing_key", self.hash_table)

    def test_should_get_value(self):
        self.assertEqual('Hello World!', self.hash_table.get('hello'))

    def test_should_return_none_with_missing_key(self):
        self.assertIsNone(self.hash_table.get("missing"))

    def test_should_return_non_default(self):
        self.assertEqual("default", self.hash_table.get("missing", "default"))

    def test_should_delete_pair(self):
        del self.hash_table['hello']
        self.assertNotIn('hello', self.hash_table)
        self.assertNotIn(('hello', 'Hello World!'), self.hash_table.array)
        self.assertEqual(2, len(self.hash_table))

    def test_delete_missing_key_should_raise_error(self):
        with self.assertRaises(KeyError) as err:
            del self.hash_table['missing']
        self.assertEqual('missing', err.exception.args[0])

    def test_should_update_value(self):
        self.hash_table['hello'] = 'Updated'
        self.assertEqual('Updated', self.hash_table['hello'])
        self.assertEqual(3, len(self.hash_table))

    def test_str(self):
        pairs = [
            "'hello': 'Hello World!'",
            "98.6: 37",
            "False: True"
        ]
        permuted_pairs = {"{" + ", ".join(p) + "}" for p in permutations(pairs)}
        self.assertIn(str(self.hash_table), permuted_pairs)


if __name__ == "__main__":
    main()