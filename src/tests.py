import unittest
from spellchecker import abspath
from markspelling import MarkSpelling


class TestFuncts(unittest.TestCase):
    """Test cases for spellchecker and markspell"""

    def setUp(self):
        """Create a shared markspell instance to use for testing"""
        self.markspell = MarkSpelling(None)

    def test_abspath(self):
        """
        Check behaviour of abspath function from main script.
        Not portable (tests assume forward-slash as seperator).
        """
        self.assertEqual(abspath('/tmp/absolute'), '/tmp/absolute')
        relative = 'relative'
        self.assertNotEqual(abspath(relative), relative)
        absolute = abspath(relative)
        self.assertTrue(absolute.endswith('/relative'))
        self.assertTrue(absolute.startswith('/'))

    def test_checkline_no_errors(self):
        """Correctly spelt lines should return no errors"""
        self.assertEqual(self.markspell.checkline('Lots of words that are spelt correctly!', 'filename.txt', False), (0, False))

    def test_checkline_one_error(self):
        """Test line with a single spelling error"""
        self.assertEqual(self.markspell.checkline('One word that is spelt icnorrectly!', 'filename.txt', False), (1, False))

    def test_checkline_multi_error(self):
        """Test line with a multiple spelling errors"""
        self.assertEqual(self.markspell.checkline('Lts of wrods thta are splet icnorrectly!', 'filename.txt', False), (5, False))

    def test_checkline_code_block_good(self):
        """Test line with no spelling errors inside a block of code"""
        self.assertEqual(self.markspell.checkline('Lots of words that are spelt correctly!', 'filename.txt', True), (0, True))

    def test_checkline_code_block_mistake(self):
        """Test that spelling errors are ignored inside a block of code"""
        self.assertEqual(self.markspell.checkline('Lots of wrods that are spelt icnorrectly!', 'filename.txt', True), (0, True))

    def test_checkline_code_block_detection(self):
        """Check that code blocks are correctly identified"""
        self.assertEqual(self.markspell.checkline('---', 'JekyllFrontMatterOpen', False), (0, True))
        self.assertEqual(self.markspell.checkline('---', 'JekyllFrontMatterClose', True), (0, False))
        self.assertEqual(self.markspell.checkline('```sh', 'GFMCodeBlockOpen', False), (0, True))
        self.assertEqual(self.markspell.checkline('```', 'GFMCodeBlockClose', True), (0, False))

    def test_checkline_backtick_good(self):
        """Test that spelling errors are not flagged by inline code snippets"""
        self.assertEqual(self.markspell.checkline('This is an example of `code within backticks`', 'filename.txt', False), (0, False))

    def test_checkline_backtick_mistake(self):
        """Test that spelling errors are ignored within inline code snippets"""
        self.assertEqual(self.markspell.checkline('This is a example of `typso niside backtciks`', 'filename.txt', False), (0, False))
        self.assertEqual(self.markspell.checkline('Outside `backtciks` speeling is still improtant', 'filename.txt', False), (2, False))

    def test_checkline_html_good(self):
        """Test that spelling errors are not flagged by inline HTML"""
        self.assertEqual(self.markspell.checkline('Test some <strong>in-line HTML</strong>', 'filename.txt', False), (0, False))
        self.assertEqual(self.markspell.checkline('Check <i>spelling witihn in-line HTML</i>', 'filename.txt', False), (1, False))

    def test_checkline_html_mistake(self):
        """Test that spelling errors are ignored within inline HTML"""
        self.assertEqual(self.markspell.checkline('Ignore <asd>bad tags</fgh>', 'filename.txt', False), (0, False))
        self.assertEqual(self.markspell.checkline('Evrething <qwe>esle mattters</rty>', 'filename.txt', False), (3, False))

if __name__ == '__main__':
    unittest.main()
