import glob
import os
import enchant
import os.path
import configparser
import json
import sys
import logging
from markspelling import MarkSpelling


def errortotalfunct(errortotal, errortotalprev, filename_jsonscore):
    logger = logging.getLogger('markdown-spellchecker')
    logger.info('Errors in total: %d', errortotal)
    if errortotal <= errortotalprev:
        logger.info('Pass. you scored better or equal to the last check')
        with open(filename_jsonscore, 'w') as outfile:
            json.dump(errortotal, outfile)
            return True
    else:
        logger.error('Fail. try harder next time')
        with open(filename_jsonscore, 'w') as outfile:
            # saves errortotal to json file for future use
            json.dump(errortotal, outfile)
            return False


def main():
    directory_self = os.path.dirname(os.path.realpath(__file__))
    directory_root = os.path.dirname(directory_self)

    config = configparser.ConfigParser()
    config.read(os.path.join(directory_self, 'config.ini'))

    logger = logging.getLogger('markdown-spellchecker')

    logger.setLevel = logging.INFO
    if config.getboolean('DEFAULT', 'log_debug'):
        logger.setLevel = logging.DEBUG

    if config.getboolean('DEFAULT', 'log_to_file'):
        logging.basicConfig(filename=os.path.join(directory_self, 'spellchecker.log'))

    directory_posts = os.path.join(directory_root, config.get('DEFAULT', 'directory_source'))
    if os.listdir(directory_posts) == []:
        logger.error('No .md files to evaluate')

    filename_jsonscore = config.get('DEFAULT', 'file_state')
    if not os.path.isabs(filename_jsonscore):
        filename_jsonscore = os.path.join(directory_self, filename_jsonscore)
    if not os.path.exists(filename_jsonscore):
        logger.warning('Please put Prevscore.json in the location of this file.')

    filename_pwl = config['DEFAULT']['personal_word_list']
    if not os.path.isabs(filename_pwl):
        filename_pwl = os.path.join(directory_self, filename_pwl)

    if os.path.exists(filename_pwl):
        logger.debug("PWL file exists")
        pwl = enchant.request_pwl_dict(filename_pwl)
    else:
        logger.error("PWL file does not exist")
        sys.exit(2)

    filenameslist = glob.glob(os.path.join(directory_posts, "*.md"))

    errortotalprev = 0
    if os.path.exists(filename_jsonscore):
        with open(filename_jsonscore, 'r') as scorefile:
            errortotalprev = json.load(scorefile)
    mspell = MarkSpelling(pwl, errortotalprev)
    errortotal = mspell.checkfilelist(filenameslist)
    passed = errortotalfunct(errortotal, errortotalprev, filename_jsonscore)
    if not passed:
        sys.exit(1)


if '__main__' == '__main__':
    main()
