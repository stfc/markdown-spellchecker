import os
import codecs
import json
import os.path
import re
import logging

class MarkSpelling(object):
    """
    Instances of MarkSpelling can be used to spell check documentation written in Markdown.
    Code snippets and in-line HTML will be excluded from checks.
    """

    def __init__(self):
        pass


    def filechecker(self, DIRECTORY_POSTS):
        if os.listdir('.') == []:
            print('Please put Prevscore.json in the location of this file.')
            return
        if os.listdir(DIRECTORY_POSTS) == []:
            print('No .md files to evaluate')
            return


    def checkline(self, line, filename, icodeblock, spellcheck, pwl, wordswrong):
        regexhtmldirty = re.compile(r'\<(?!\!--)(.*?)\>')
        regexhtmlclean = re.compile(r'\`.*?\`')
        logger = logging.getLogger('markdown-spellchecker')
        logger.info('now checking file %s', filename)
        error = 0
        skipline = False  # defaults to not skip line
        if line.startswith('```') or line == '---':
            icodeblock = not icodeblock
        if icodeblock:
            skipline = True
        if not icodeblock and not skipline:
            htmldirty = regexhtmldirty.sub('', line)  # strips code between < >
            cleanhtml = regexhtmlclean.sub('', htmldirty)  # strips code between ` `
            spellcheck.set_text(cleanhtml)
            for err in spellcheck:
                logger.debug("'%s' not found in main dictionary", err.word)
                if not pwl.check(err.word):
                    error += 1
                    wordswrong.write('%s in %s\n' % (err.word, filename))
                    print('Failed word: ', err.word)
        return error


    def checkfile(self, filename, pwl, filecheck, wordswrong, spellcheck,):
        error = 0
        icodeblock = False
        linelist = codecs.open(filename, 'r', encoding='UTF-8').readlines()
        for line in linelist:
            error += self.checkline(line, filename, icodeblock, spellcheck, pwl, wordswrong)
        print(error, ' errors in total in ', filename)
        filecheck.write('%d errors in total in %s\n' % (error, filename))
        return error


    def linechecker(self, errortotalprev, pwl, filenameslist, filecheck, wordswrong, spellcheck, FILENAME_JSONSCORE):
        errortotal = 0
        for filename in filenameslist:
            errortotal += self.checkfile(filename, pwl, filecheck, wordswrong, spellcheck)

        return self.errortotalfunct(errortotal, errortotalprev, FILENAME_JSONSCORE)


    def errortotalfunct(self, errortotal, errortotalprev, FILENAME_JSONSCORE):
        print('Errors in total: ', errortotal)
        if errortotal <= errortotalprev:
            print('Pass. you scored better or equal to the last check')
            with open(FILENAME_JSONSCORE, 'w') as outfile:
                json.dump(errortotal, outfile)
                return True
        else:
            print('Fail. try harder next time')
            with open(FILENAME_JSONSCORE, 'w') as outfile:
                # saves errortotal to json file for future use
                json.dump(errortotal, outfile)
                return False
