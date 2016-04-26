import unittest
import logging
from spellchecker import abspath
from markspelling import MarkSpelling


class TestFuncts(unittest.TestCase):
    """Test cases for spellchecker and markspell"""

    def setUp(self):
        """Create a shared markspell instance to use for testing"""
        logging.basicConfig(level=logging.WARNING, format='%(levelname)6s: %(message)s')
        self.logger = logging.getLogger('markdown-spellchecker')
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
        self.assertEqual(self.markspell.checkline('Lots of words that are spelt correctly!', False), (0, False))

    def test_checkline_one_error(self):
        """Test line with a single spelling error"""
        self.assertEqual(self.markspell.checkline('One word that is spelt icnorrectly!', False), (1, False))

    def test_checkline_multi_error(self):
        """Test line with a multiple spelling errors"""
        self.assertEqual(self.markspell.checkline('Lts of wrods thta are splet icnorrectly!', False), (5, False))

    def test_checkline_code_block_good(self):
        """Test line with no spelling errors inside a block of code"""
        self.assertEqual(self.markspell.checkline('Lots of words that are spelt correctly!', True), (0, True))

    def test_checkline_code_block_mistake(self):
        """Test that spelling errors are ignored inside a block of code"""
        self.assertEqual(self.markspell.checkline('Lots of wrods that are spelt icnorrectly!', True), (0, True))

    def test_checkline_code_block_detection(self):
        """Check that code blocks are correctly identified"""
        # Jekyll front matter
        self.assertEqual(self.markspell.checkline('---', False), (0, True))
        self.assertEqual(self.markspell.checkline('---', True), (0, False))
        # Github flavoured markdown code blocks
        self.assertEqual(self.markspell.checkline('```sh', False), (0, True))
        self.assertEqual(self.markspell.checkline('```', True), (0, False))

    def test_checkline_backtick_good(self):
        """Test that spelling errors are not flagged by inline code snippets"""
        self.assertEqual(self.markspell.checkline('This is an example of `code within backticks`', False), (0, False))

    def test_checkline_backtick_mistake(self):
        """Test that spelling errors are ignored within inline code snippets"""
        self.assertEqual(self.markspell.checkline('This is a example of `typso niside backtciks`', False), (0, False))
        self.assertEqual(self.markspell.checkline('Outside `backtciks` speeling is still improtant', False), (2, False))

    def test_checkline_html_good(self):
        """Test that spelling errors are not flagged by inline HTML"""
        self.assertEqual(self.markspell.checkline('Test some <strong>in-line HTML</strong>', False), (0, False))
        self.assertEqual(self.markspell.checkline('Check <i>spelling witihn in-line HTML</i>', False), (1, False))

    def test_checkline_html_mistake(self):
        """Test that spelling errors are ignored within inline HTML"""
        self.assertEqual(self.markspell.checkline('Ignore <asd>bad tags</fgh>', False), (0, False))
        self.assertEqual(self.markspell.checkline('Evrething <qwe>esle mattters</rty>', False), (3, False))

    def test_checklinelist(self):
        """Check a list of lines for correct behaviour"""
        lines = [
            'Correct spelling is important in documentation.',
            '',
            '```python',
            '    # But not necesssatily in blcoks of code!',
            '```',
            '',
            'Woohps.',
        ]
        self.assertEqual(self.markspell.checklinelist(lines), 1)

    def test_checkfile(self):
        """Check an example file"""
        self.logger.setLevel(logging.DEBUG)
        self.assertEqual(self.markspell.checkfile(abspath('testfile.md')), 0)
        self.logger.setLevel(logging.WARNING)

if __name__ == '__main__':
    unittest.main()
