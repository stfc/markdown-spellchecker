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

    def checkline(self, line, filename, icodeblock):
        regexhtmldirty = re.compile(r'\<(?!\!--)(.*?)\>')
        regexhtmlclean = re.compile(r'\`.*?\`')
        self.logger.debug('Checking file %s', filename)
        error = 0
        skipline = False  # defaults to not skip line
        if line.startswith('```') or line == '---':
            icodeblock = not icodeblock
        if icodeblock:
            skipline = True
        if not icodeblock and not skipline:
            htmldirty = regexhtmldirty.sub('', line)  # strip html tags
            cleanhtml = regexhtmlclean.sub('', htmldirty)  # strip inline code
            self.spellcheck.set_text(cleanhtml)
            for err in self.spellcheck:
                self.logger.debug("'%s' not found in main dictionary", err.word)
                if not self.pwl or not self.pwl.check(err.word):
                    error += 1
                    self.logger.info('Failed word "%s" in %s', err.word, filename)
        return error

    def checkfile(self, filename):
        error = 0
        icodeblock = False
        linelist = codecs.open(filename, 'r', encoding='UTF-8').readlines()
        for line in linelist:
            error += self.checkline(line, filename, icodeblock)
        self.logger.info('%d errors in total in %s', error, filename)
        return error

    def checkfilelist(self, filenameslist):
        for filename in filenameslist:
            self.errortotal += self.checkfile(filename)

        return self.errortotal
