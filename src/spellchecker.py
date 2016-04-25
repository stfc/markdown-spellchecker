import glob
import os
import enchant
import os.path
import configparser
import json
from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter
import sys
from markspelling import MarkSpelling

DIRECTORY_SELF = os.path.dirname(os.path.realpath(__file__))
DIRECTORY_ROOT = os.path.dirname(DIRECTORY_SELF)

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(DIRECTORY_SELF, 'config.ini'))
DEFAULTCONFIGFILE = CONFIG['DEFAULT']

DIRECTORY_POSTS = os.path.join(DIRECTORY_ROOT, DEFAULTCONFIGFILE['Filestocheckdir'])
if os.listdir(DIRECTORY_POSTS) == []:
    print('No .md files to evaluate')

FILENAME_JSONSCORE = DEFAULTCONFIGFILE['Prevscore']
if not os.path.isabs(FILENAME_JSONSCORE):
    FILENAME_JSONSCORE = os.path.join(DIRECTORY_SELF, DEFAULTCONFIGFILE['Prevscore'])
if not os.path.exists(FILENAME_JSONSCORE):
    print('Please put Prevscore.json in the location of this file.')

FILENAME_PWL = DEFAULTCONFIGFILE['PWL']
if not os.path.isabs(FILENAME_PWL):
    FILENAME_PWL = os.path.join(DIRECTORY_SELF, DEFAULTCONFIGFILE['PWL'])

if os.path.exists(FILENAME_PWL):
    print("PWL file exists")
    pwl = enchant.request_pwl_dict(FILENAME_PWL)
    print("Loaded PWL object: %s" % pwl)
    print("Methods of object: %s" % dir(pwl))
else:
    print("PWL file does not exist")
    sys.exit(2)

filenameslist = glob.glob(os.path.join(DIRECTORY_POSTS, "*.md"))
wordswrong = open(CONFIG['DEFAULT']['Wordswrongfile'], "w+") # Log of incorrectly spelt words
filecheck = open(CONFIG['DEFAULT']['Filecheck'], "w+") # Log of files that were checked


def errortotalfunct(errortotal, errortotalprev):
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


def main():
    errortotalprev = 0
    if os.path.exists(FILENAME_JSONSCORE):
        with open(FILENAME_JSONSCORE, 'r') as scorefile:
            errortotalprev = json.load(scorefile)
    spellcheck = SpellChecker("en_GB", filters=[URLFilter, EmailFilter])
    mspell = MarkSpelling(DIRECTORY_POSTS, spellcheck, pwl, filecheck, wordswrong, errortotalprev)
    errortotal = mspell.checkfilelist(filenameslist)
    passed = errortotalfunct(errortotal, errortotalprev)
    filecheck.close()
    wordswrong.close()
    if not passed:
        sys.exit(1)


if '__main__' == '__main__':
    main()
