# setting the PATH seems only to work in GNUmake not in BSDmake
PATH := ./pythonenv/bin:$(PATH)

default: check test examples

check:
	pep8 -r --ignore=E501,E111 huTools/
	-pyflakes $$(find huTools -name '*.py' | grep -v 'http\/__init' | grep -v 'http\/_httplib2')
	-pylint -iy --max-line-length=110 --ignore=_httplib2 huTools

test: dependencies
	PYTHONPATH=. coverage run huTools/aggregation.py
	#PYTHONPATH=. ./pythonenv/bin/python huTools/http/test.py
	PYTHONPATH=. coverage run huTools/NetStringIO.py
	PYTHONPATH=. coverage run huTools/calendar/formats.py
	PYTHONPATH=. coverage run huTools/calendar/tools.py
	PYTHONPATH=. coverage run huTools/calendar/workdays.py
	PYTHONPATH=. coverage run huTools/checksumming.py
	PYTHONPATH=. coverage run huTools/humessaging.py
	PYTHONPATH=. coverage run huTools/luids.py
	PYTHONPATH=. coverage run huTools/obfuscation.py
	PYTHONPATH=. coverage run huTools/postmark.py
	PYTHONPATH=. coverage run huTools/structured.py
	PYTHONPATH=. coverage run huTools/unicode.py
	#PYJASPER_SERVLET_URL=http://127.0.0.1:8000/pyJasper/jasper.py PYTHONPATH=. ./pythonenv/bin/python huTools/pyjasper.py

upload:
	rm -Rf build dist
	python setup.py sdist
	VERSION=`ls dist/ | perl -npe 's/.*-(\d+\..*?).tar.gz/$1/' | sort | tail -n 1`
	python setup.py sdist upload
	git tag v$(VERSION)
	git push origin --tags
	git commit -m "v$(VERSION) published on PyPi" -a
	git push origin

build:
	python setup.py build

dependencies: pythonenv/bin/python

pythonenv/bin/python:
	pip -q install -r requirements.txt

doc: examples
	paver gh_pages_build gh_pages_update -m "documentation fixup"

install: build
	sudo python setup.py install

clean:
	rm -Rf testenv pythonenv build dist html test.db pylint.out sloccount.sc pip-log.txt
	find . -name '*.pyc' -delete

.PHONY: build clean install upload check doc docs test
