SHELL = /bin/sh +x
VIRTUALENV_NAME ?= content_analytics

# Each of your targets should be listed as .PHONY (unless you are actually
# compiling a C source file or similar)
# :r! grep '^[a-z-]\+:' % | cut -d: -f1 | sort
.PHONY: config edit install requirements test virtualenv
# first target is default, let it be something harmless
config:

install: virtualenv
	. ./bin/activate

test:
	. ./bin/activate && nosetests  -sv ./app/test/

virtualenv:
	virtualenv --python=python2.7 --no-site-packages --setuptools --prompt="[$(VIRTUALENV_NAME)]" . && \
	. ./bin/activate && pip install -r requirements.txt
