import unittest
import enchant
from tempfile import TemporaryFile
from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter
from funct import checkline
from funct import filechecker

class TestFuncts(unittest.TestCase):

    def test_checkline_no_errors(self):
        checker = SpellChecker("en_GB", filters=[URLFilter, EmailFilter])
        pwl = enchant.request_pwl_dict('dict.txt')
        with TemporaryFile('w') as tfile:
            self.assertEqual(checkline('Lots of words that are spelt correctly!', 'filename.txt', False, checker, pwl, tfile), 0)


    def test_checkline_one_error(self):
        checker = SpellChecker("en_GB", filters=[URLFilter, EmailFilter])
        pwl = enchant.request_pwl_dict('dict.txt')
        with TemporaryFile('w') as tfile:
            self.assertEqual(checkline('Lots of words that are spelt orrectly!', 'filename.txt', False, checker, pwl, tfile), 1)


    def test_checkline_code_block_good(self):
        checker = SpellChecker("en_GB", filters=[URLFilter, EmailFilter])
        pwl = enchant.request_pwl_dict('dict.txt')
        with TemporaryFile('w') as tfile:
            self.assertEqual(checkline('Lots of words that are spelt correctly!', 'filename.txt', True, checker, pwl, tfile), 0)


    def test_checkline_code_block_mistake(self):
        checker = SpellChecker("en_GB", filters=[URLFilter, EmailFilter])
        pwl = enchant.request_pwl_dict('dict.txt')
        with TemporaryFile('w') as tfile:
            self.assertEqual(checkline('Lots of words that are spelt orrectly!', 'filename.txt', True, checker, pwl, tfile), 0)

if __name__ == '__main__':
    unittest.main()
