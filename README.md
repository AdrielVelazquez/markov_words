Markov Words
===========

Markov Chains (Word Finder)

Description
===========
This application is a method of finding if words are english language words
https://github.com/AdrielVelazquez/markov_words
The application for the trainer pulls heavily from
https://github.com/rrenaud/Gibberish-Detector/blob/master/gib_detect_train.py

System Dependencies
===================
Some Common System dependencies are the following.
sudo apt-get install <package>

Python 2.7.3 (available via apt in debian "wheezy") or 2.7.5+ (in ubuntu 13.10)
pip 1.1 (available via apt in debian wheezy as python-pip)
git
libbz2-dev
libffi-dev
libicu-dev
libjpeg-dev
libpython-dev

The application references the

Will setup virtualenv and pip requirements
==========================================
make install

will run unittests
==================
make test

Initiate virtualenv - after make install
========================================
. ./bin/activate 

Run program
===========
python server.py


