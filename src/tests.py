import unittest
import enchant
import tempfile
from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter
from funct import checkline

class TestFuncts(unittest.TestCase):

    def test_checkline(self):
        checker = SpellChecker("en_GB", filters=[URLFilter, EmailFilter])
        pwl = enchant.request_pwl_dict('dict.txt')
        tfile = tempfile.TemporaryFile()

        self.assertEqual(checkline('Lots of words that are spelt correctly!', 'filename.txt', False, checker, pwl, tfile), 0)


if __name__ == '__main__':
    unittest.main()
