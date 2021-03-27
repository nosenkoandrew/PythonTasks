import unittest
from ..anagrams import task1


cases = [
        ("a1bcd efg!h", "d1cba hgf!e"),
        ("abcd efgh", "dcba hgfe"),
        ('', ''),
    ]

class TestAnagrams(unittest.TestCase):
    def test_anagrams(self):
        for in_data, out_data in cases:
            with self.subTest():
                res = task1.reverseOnlyLetters(in_data)
                self.assertEqual(out_data, res)


if __name__ == "__main__":
    unittest.main()



