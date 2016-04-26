import glob
import os
import enchant
import os.path
import configparser
import json
import sys
import logging
from markspelling import MarkSpelling


def errortotalfunct(errortotal, errortotalprev, file_state):
    logger = logging.getLogger('markdown-spellchecker')
    logger.info('Errors in total: %d', errortotal)
    if errortotal <= errortotalprev:
        logger.info('Pass. you scored better or equal to the last check')
        with open(file_state, 'w') as outfile:
            json.dump(errortotal, outfile)
            return True
    else:
        logger.error('Fail. try harder next time')
        with open(file_state, 'w') as outfile:
            # saves errortotal to json file for future use
            json.dump(errortotal, outfile)
            return False


def abspath(path):
    """Return an absolute form of path relative to this script"""
    root = os.path.dirname(os.path.realpath(__file__))
    if not os.path.isabs(path):
        path = os.path.join(root, path)
    return path


def main():
    config = configparser.ConfigParser()
    config.read(abspath('config.ini'))

    logger = logging.getLogger('markdown-spellchecker')

    logger.setLevel = logging.INFO
    if config.getboolean('DEFAULT', 'log_debug'):
        logger.setLevel = logging.DEBUG

    if config.getboolean('DEFAULT', 'log_to_file'):
        logging.basicConfig(filename=abspath('spellchecker.log'))

    directory_source = abspath(config.get('DEFAULT', 'directory_source'))
    file_state = abspath(config.get('DEFAULT', 'file_state'))
    personal_word_list = abspath(config.get('DEFAULT', 'personal_word_list'))

    if not os.path.exists(directory_source):
        logger.error('Source directory "%s" does not exist', directory_source)
        sys.exit(1)

    if os.listdir(directory_source) == []:
        logger.error('No .md files to evaluate')
        sys.exit(1)

    pwl = None
    if os.path.exists(personal_word_list):
        logger.debug("PWL file exists")
        pwl = enchant.request_pwl_dict(personal_word_list)
    else:
        logger.error("PWL file does not exist")
        sys.exit(1)

    filenameslist = glob.glob(os.path.join(directory_source, "*.md"))

    errortotalprev = 0
    try:
        with open(file_state, 'r') as scorefile:
            errortotalprev = json.load(scorefile)
    except FileNotFoundError:
        logger.warning('JSON score file "%s" was not found', file_state)
    mspell = MarkSpelling(pwl, config.get('DEFAULT', 'spelling_language'), errortotalprev)
    errortotal = mspell.checkfilelist(filenameslist)
    passed = errortotalfunct(errortotal, errortotalprev, file_state)
    if not passed:
        sys.exit(1)


if '__main__' == '__main__':
    main()
