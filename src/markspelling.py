import codecs
import re
from logging import getLogger
from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter


class MarkSpelling(object):
    """
    Instances of MarkSpelling can be used to spell check documentation written in Markdown.
    Code snippets and in-line HTML will be excluded from checks.
    """

    def __init__(self, pwl, language='en_GB', errortotalprev=0):
        self.logger = getLogger('markdown-spellchecker')
        self.spellcheck = SpellChecker(language, filters=[URLFilter, EmailFilter])
        self.pwl = pwl
        self.errortotalprev = errortotalprev
        self.errortotal = 0
        self.regexhtmldirty = re.compile(r'\<(?!\!--)(.*?)\>')
        self.regexhtmlclean = re.compile(r'\`.*?\`')

    def checkcodeblock(self, line, incodeblock):
        if line.startswith('```') or line == '---':
            return not incodeblock
        return incodeblock

    def checkline(self, line, incodeblock=False):
        line = line.strip()
        errorcount = 0
        wasincodeblock = incodeblock
        incodeblock = self.checkcodeblock(line, incodeblock)
        if not wasincodeblock and not incodeblock:
            self.logger.debug('Checking line "%s"', line.rstrip())
            line = self.regexhtmldirty.sub('', line)  # strip html tags
            line = self.regexhtmlclean.sub('', line)  # strip inline code
            self.spellcheck.set_text(line)
            for err in self.spellcheck:
                self.logger.debug("'%s' not found in main dictionary", err.word)
                if not self.pwl or not self.pwl.check(err.word):
                    errorcount += 1
                    self.logger.info('Failed word "%s"', err.word)
        else:
            self.logger.debug('Skipping line "%s"', line.rstrip())

        return (errorcount, incodeblock)

    def checklinelist(self, linelist):
        errorcount = 0
        incodeblock = False
        for line in linelist:
            (lineerrors, incodeblock) = self.checkline(line, incodeblock)
            errorcount += lineerrors
        return errorcount

    def checkfile(self, filename):
        self.logger.debug('Checking file "%s"', filename)
        lines = codecs.open(filename, 'r', encoding='UTF-8').readlines()
        fileerrors = self.checklinelist(lines)
        self.logger.info('%d errors in total in %s', fileerrors, filename)
        return fileerrors

    def checkfilelist(self, filenameslist):
        for filename in filenameslist:
            self.errortotal += self.checkfile(filename)

        return self.errortotal
