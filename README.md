Markdown Spellchecker
=====================

[![Code Climate](https://codeclimate.com/github/stfc/markdown-spellchecker/badges/gpa.svg)](https://codeclimate.com/github/stfc/markdown-spellchecker)
[![Build Status](https://travis-ci.org/stfc/markdown-spellchecker.svg?branch=master)](https://travis-ci.org/stfc/markdown-spellchecker)
[![Coverage Status](https://coveralls.io/repos/github/stfc/markdown-spellchecker/badge.svg?branch=master)](https://coveralls.io/github/stfc/markdown-spellchecker?branch=master)

What is it?
* This program is a spellchecker made in python to check .md documents for spelling errors outside of code.

What is needed for this?
* Python
* Pyenchant

Why use it?
* It dosent check words inside of codeblocks.
* It can also have technical words added to the PWL exclude them from the spellcheck.
* It also dosent check the code inside of HTML tags.

How to install?
*
*

What is the PWL?
* PWL is the personal word list.
* It is used to store words that the dictionary would say are spelt wrong.
* to exclude a word add it to "dict.txt" which you can specify what its called as long as you change it in the config.

How to configure it?
* Go into "config.ini"
* you can change where it finds the the documents to check.
* the personal word list.
* the name of the text file it creates to tell you which files its checked.
* The name of the text file it creates to tell you which spellings are wrong.

What are the advantages of this program and why did I bother making it??
* Saves Previous score so it can be used to compare to your previous score and how well you have done.
* It dosent check words inside of codeblocks or technical words that can be specified in the PWL document.
* It can check things inside of HTML notes

What about grammar?
* Yeah... how about no.

How to use it?
* To use it run spellchecker.py in this file structure: `./_tests/`
* keep the posts in the .md type file in the user defined space where it should be `./_posts` (or whatever you set it to)

Anything else I should know?
* Keep "dict.txt" with the python files.
* if dict.txt dosent exist create a document for it.
* Add words that you dont want spellchecked in the file too.
