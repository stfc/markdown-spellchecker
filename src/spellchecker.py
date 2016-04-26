#!/usr/bin/env python3
import glob
import os
import enchant
import os.path
import configparser
import json
import sys
import logging
from markspelling import MarkSpelling


def configurelogger(config):
    log_format = '%(levelname)6s: %(message)s'
    log_level = logging.INFO
    log_file = ''

    if config.getboolean('DEFAULT', 'log_debug'):
        log_level = logging.DEBUG

    if config.getboolean('DEFAULT', 'log_to_file'):
        log_file = abspath('spellchecker.log')

    logging.basicConfig(level=log_level, format=log_format, filename=log_file)

    return logging.getLogger('markdown-spellchecker')


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


def verifydirectorysource(path):
    logger = logging.getLogger('markdown-spellchecker')
    if not os.path.exists(path):
        logger.error('Source directory "%s" does not exist', path)
        sys.exit(1)

    if os.listdir(path) == []:
        logger.error('No .md files to evaluate')
        sys.exit(1)


def loadpwl(filename):
    logger = logging.getLogger('markdown-spellchecker')
    if os.path.exists(filename):
        logger.debug('PWL file found')
        pwl = enchant.request_pwl_dict(filename)
        logger.debug('PWL file loaded')
        return pwl
    else:
        logger.error('PWL file "%s" does not exist', filename)
        sys.exit(1)
    return None


def getfilenameslist(path):
    return glob.glob(os.path.join(path, "*.md"))


def main():
    config = configparser.ConfigParser()
    config.read(abspath('config.ini'))

    logger = configurelogger(config)

    directory_source = abspath(config.get('DEFAULT', 'directory_source'))
    file_state = abspath(config.get('DEFAULT', 'file_state'))
    personal_word_list = abspath(config.get('DEFAULT', 'personal_word_list'))
    spelling_language = config.get('DEFAULT', 'spelling_language')

    verifydirectorysource(directory_source)

    pwl = loadpwl(personal_word_list)

    filenameslist = getfilenameslist(directory_source)

    errortotalprev = 0
    try:
        with open(file_state, 'r') as scorefile:
            errortotalprev = json.load(scorefile)
    except FileNotFoundError:
        logger.warning('JSON score file "%s" was not found', file_state)

    mspell = MarkSpelling(pwl, spelling_language, errortotalprev)
    errortotal = mspell.checkfilelist(filenameslist)
    passed = errortotalfunct(errortotal, errortotalprev, file_state)
    if not passed:
        sys.exit(1)


if __name__ == '__main__':
    main()
