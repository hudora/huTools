# setting the PATH seems only to work in GNUmake not in BSDmake
PATH := ./pythonenv/bin:$(PATH)

default: dependencies check test examples

hudson: dependencies test statistics coverage
	find huTools -name '*.py' | xargs /usr/local/hudorakit/bin/hd_pep8
	/usr/local/hudorakit/bin/hd_pylint huTools
	# we can't use tee because it eats the error code from hd_pylint
	/usr/local/hudorakit/bin/hd_pylint -f parseable huTools > .pylint.out
	printf 'YVALUE=' > .pylint.score
	grep "our code has been rated at" < .pylint.out|cut -d '/' -f 1|cut -d ' ' -f 7 >> .pylint.score

check:
	-find huTools -name '*.py' | xargs /usr/local/hudorakit/bin/hd_pep8
	-/usr/local/hudorakit/bin/hd_pylint huTools

test:
	PYTHONPATH=. ./pythonenv/bin/python huTools/http/test.py
	PYTHONPATH=. ./pythonenv/bin/python huTools/NetStringIO.py
	PYTHONPATH=. ./pythonenv/bin/python huTools/calendar/formats.py
	PYTHONPATH=. ./pythonenv/bin/python huTools/calendar/workdays.py
	PYTHONPATH=. ./pythonenv/bin/python huTools/checksumming.py
	PYTHONPATH=. ./pythonenv/bin/python huTools/humessaging.py
	PYTHONPATH=. ./pythonenv/bin/python huTools/luids.py
	PYTHONPATH=. ./pythonenv/bin/python huTools/obfuscation.py
	PYTHONPATH=. ./pythonenv/bin/python huTools/unicode.py
	PYJASPER_SERVLET_URL=http://127.0.0.1:8000/pyJasper/jasper.py PYTHONPATH=. ./pythonenv/bin/python huTools/pyjasper.py

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

build: examples
	python setup.py build

dependencies:
	virtualenv pythonenv
	pip -q install -E pythonenv -r requirements.txt

statistics:
	sloccount --wide --details huTools | tee sloccount.sc

upload: doc
	python setup.py build sdist upload

doc: examples
	paver gh_pages_build gh_pages_update -m "documentation fixup"

install: build
	sudo python setup.py install

doc/standards/examples/%.xml: doc/standards/examples/%.json
	python huTools/protocols.py $<  | xmllint --encode utf-8 --format - > $@

examples: doc/standards/examples/warenzugang.xml doc/standards/examples/kommiauftrag.xml doc/standards/examples/rueckmeldung.xml doc/standards/examples/wms2logos_warenzugang.xslt doc/standards/examples/wms2logos_kommiauftrag.xslt
	xsltproc doc/standards/examples/wms2logos_warenzugang.xslt doc/standards/examples/warenzugang.xml > doc/standards/examples/wms2logos_warenzugang.xml
	xsltproc doc/standards/examples/wms2logos_kommiauftrag.xslt doc/standards/examples/kommiauftrag.xml > doc/standards/examples/wms2logos_kommiauftrag.xml


clean:
	rm -Rf testenv pythonenv build dist html test.db pylint.out sloccount.sc pip-log.txt
	find . -name '*.pyc' -delete

.PHONY: build clean install upload check doc docs test
