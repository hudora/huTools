# setting the PATH seems only to work in GNUmake not in BSDmake
PATH := ./pythonenv/bin:$(PATH)

default: check test examples

check:
	pep8 -r --ignore=E501,E111 huTools/
	-pyflakes huTools
	# Zeilen laenger als 110 Zeichen
	find huTools/ -name '*.py' -exec awk 'length > 110' {} \;
	test 0 = `find huTools/ -name '*.py' -exec awk 'length > 110' {} \; | wc -l`
	# pyLint
	-pylint -iy --max-line-length=110 --ignore=_httplib2 huTools

test: dependencies
	PYTHONPATH=. ./pythonenv/bin/python huTools/http/test.py
	PYTHONPATH=. ./pythonenv/bin/python huTools/NetStringIO.py
	PYTHONPATH=. ./pythonenv/bin/python huTools/calendar/formats.py
	PYTHONPATH=. ./pythonenv/bin/python huTools/calendar/workdays.py
	PYTHONPATH=. ./pythonenv/bin/python huTools/checksumming.py
	PYTHONPATH=. ./pythonenv/bin/python huTools/humessaging.py
	PYTHONPATH=. ./pythonenv/bin/python huTools/luids.py
	PYTHONPATH=. ./pythonenv/bin/python huTools/obfuscation.py
	PYTHONPATH=. ./pythonenv/bin/python huTools/postmark.py
	PYTHONPATH=. ./pythonenv/bin/python huTools/structured.py
	PYTHONPATH=. ./pythonenv/bin/python huTools/unicode.py
	#PYJASPER_SERVLET_URL=http://127.0.0.1:8000/pyJasper/jasper.py PYTHONPATH=. ./pythonenv/bin/python huTools/pyjasper.py

coverage: dependencies
	printf '.*/tests/.*\n.*test.py\n' > .figleaf-exclude.txt
	printf '/usr/local/lib/.*\n/opt/.*\npythonenv/.*\n' >> .figleaf-exclude.txt
	printf '.*manage.py\n.*settings.py\n.*setup.py\n.*urls.py\n' >> .figleaf-exclude.txt
	PYTHONPATH=. /usr/local/hudorakit/bin/hd_figleaf --ignore-pylibs huTools/NetStringIO.py
	PYTHONPATH=. /usr/local/hudorakit/bin/hd_figleaf --ignore-pylibs huTools/ReReadingConfigParser.py
	PYTHONPATH=. /usr/local/hudorakit/bin/hd_figleaf --ignore-pylibs huTools/async.py
	PYTHONPATH=. /usr/local/hudorakit/bin/hd_figleaf --ignore-pylibs huTools/calendar/formats.py
	PYTHONPATH=. /usr/local/hudorakit/bin/hd_figleaf --ignore-pylibs huTools/calendar/workdays.py
	PYTHONPATH=. /usr/local/hudorakit/bin/hd_figleaf --ignore-pylibs huTools/checksumming.py
	PYTHONPATH=. /usr/local/hudorakit/bin/hd_figleaf --ignore-pylibs huTools/daemon.py
	PYTHONPATH=. /usr/local/hudorakit/bin/hd_figleaf --ignore-pylibs huTools/decorators.py
	PYTHONPATH=. /usr/local/hudorakit/bin/hd_figleaf --ignore-pylibs huTools/fs.py
	PYTHONPATH=. /usr/local/hudorakit/bin/hd_figleaf --ignore-pylibs huTools/luids.py
	PYTHONPATH=. /usr/local/hudorakit/bin/hd_figleaf --ignore-pylibs huTools/obfuscation.py
	PYTHONPATH=. /usr/local/hudorakit/bin/hd_figleaf --ignore-pylibs huTools/printing.py
	PYTHONPATH=. /usr/local/hudorakit/bin/hd_figleaf --ignore-pylibs huTools/robusttypecasts.py
	PYTHONPATH=. /usr/local/hudorakit/bin/hd_figleaf --ignore-pylibs huTools/unicode.py
	python /usr/local/hudorakit/bin/hd_figleaf2html -d ./coverage -x .figleaf-exclude.txt
	echo "Coverage: " `grep -A3 ">totals:<" coverage/index.html|tail -n1|cut -c 9-13|cut -d'<' -f1`
	test `grep -A3 ">totals:<" coverage/index.html|tail -n1|cut -c 9-13|cut -d'.' -f1` -gt 70
	printf 'YVALUE=' > .coverage.score
	grep -A3 ">totals:<" coverage/index.html|tail -n1|cut -c 9-12 >> .coverage.score

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
	virtualenv pythonenv
	pip -q install -E pythonenv -r requirements.txt

doc: examples
	paver gh_pages_build gh_pages_update -m "documentation fixup"

install: build
	sudo python setup.py install

clean:
	rm -Rf testenv pythonenv build dist html test.db pylint.out sloccount.sc pip-log.txt
	find . -name '*.pyc' -delete

.PHONY: build clean install upload check doc docs test
