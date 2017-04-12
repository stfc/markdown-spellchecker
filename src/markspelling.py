# Copyright 2016 Science & Technology Facilities Council
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

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

    def checkline(self, line, linenumber, incodeblock=False):
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
                    self.logger.info('%s : "%s"', linenumber, err.word)
        else:
            self.logger.debug('Skipping line "%s"', line.rstrip())

        return (errorcount, incodeblock)

    def checklinelist(self, linelist):
        errorcount = 0
        incodeblock = False
        for linenumber, line in enumerate(linelist):
            (lineerrors, incodeblock) = self.checkline(line, linenumber, incodeblock)
            errorcount += lineerrors
        return errorcount

    def checkfile(self, filename):
        self.logger.debug('Checking file "%s"', filename)
        fileerrors = 0
        with codecs.open(filename, 'r', encoding='UTF-8') as markdownfile:
            lines = markdownfile.readlines()
            fileerrors = self.checklinelist(lines)
        self.logger.info('%d errors in total in %s', fileerrors, filename)
        return fileerrors

    def checkfilelist(self, filenameslist):
        for filename in filenameslist:
            self.errortotal += self.checkfile(filename)

        return self.errortotal
