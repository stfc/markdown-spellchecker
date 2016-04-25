import codecs
import re
from logging import getLogger

class MarkSpelling(object):
    """
    Instances of MarkSpelling can be used to spell check documentation written in Markdown.
    Code snippets and in-line HTML will be excluded from checks.
    """

    def __init__(self, DIRECTORY_POSTS, spellcheck, pwl, filecheck, wordswrong, errortotalprev = 0):
        self.logger = getLogger('markdown-spellchecker')
        self.DIRECTORY_POSTS = DIRECTORY_POSTS
        self.spellcheck = spellcheck
        self.pwl = pwl
        self.filecheck = filecheck
        self.wordswrong = wordswrong
        self.errortotalprev = errortotalprev
        self.errortotal = 0


    def checkline(self, line, filename, icodeblock):
        regexhtmldirty = re.compile(r'\<(?!\!--)(.*?)\>')
        regexhtmlclean = re.compile(r'\`.*?\`')
        self.logger.info('now checking file %s', filename)
        error = 0
        skipline = False  # defaults to not skip line
        if line.startswith('```') or line == '---':
            icodeblock = not icodeblock
        if icodeblock:
            skipline = True
        if not icodeblock and not skipline:
            htmldirty = regexhtmldirty.sub('', line)  # strips code between < >
            cleanhtml = regexhtmlclean.sub('', htmldirty)  # strips code between ` `
            self.spellcheck.set_text(cleanhtml)
            for err in self.spellcheck:
                self.logger.debug("'%s' not found in main dictionary", err.word)
                if not self.pwl.check(err.word):
                    error += 1
                    self.wordswrong.write('%s in %s\n' % (err.word, filename))
                    self.logger.debug('Failed word: %s', err.word)
        return error


    def checkfile(self, filename):
        error = 0
        icodeblock = False
        linelist = codecs.open(filename, 'r', encoding='UTF-8').readlines()
        for line in linelist:
            error += self.checkline(line, filename, icodeblock)
        self.logger.info('%d errors in total in %s', error, filename)
        self.filecheck.write('%d errors in total in %s\n' % (error, filename))
        return error


    def checkfilelist(self, filenameslist):
        for filename in filenameslist:
            self.errortotal += self.checkfile(filename)

        return self.errortotal
