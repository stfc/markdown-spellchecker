import unittest
import enchant
from markspelling import MarkSpelling

class TestFuncts(unittest.TestCase):

    def test_checkline_no_errors(self):
        pwl = enchant.request_pwl_dict('dict.txt')
        markspell = MarkSpelling(pwl)
        self.assertEqual(markspell.checkline('Lots of words that are spelt correctly!', 'filename.txt', False), 0)


    def test_checkline_one_error(self):
        pwl = enchant.request_pwl_dict('dict.txt')
        markspell = MarkSpelling(pwl)
        self.assertEqual(markspell.checkline('Lots of words that are spelt orrectly!', 'filename.txt', False), 1)


    def test_checkline_code_block_good(self):
        pwl = enchant.request_pwl_dict('dict.txt')
        markspell = MarkSpelling(pwl)
        self.assertEqual(markspell.checkline('Lots of words that are spelt correctly!', 'filename.txt', True), 0)


    def test_checkline_code_block_mistake(self):
        pwl = enchant.request_pwl_dict('dict.txt')
        markspell = MarkSpelling(pwl)
        self.assertEqual(markspell.checkline('Lots of words that are spelt orrectly!', 'filename.txt', True), 0)

if __name__ == '__main__':
    unittest.main()
