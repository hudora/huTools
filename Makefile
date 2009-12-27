# setting the PATH seems only to work in GNUmake not in BSDmake
PATH := ./testenv/bin:$(PATH)

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
	PYTHONPATH=. python huTools/humessaging.py
	PYTHONPATH=. python huTools/luids.py
	PYTHONPATH=. python huTools/checksumming.py
	PYTHONPATH=. python huTools/calendar/workdays.py
	PYTHONPATH=. python huTools/calendar/formats.py
	PYTHONPATH=. python huTools/obfuscation.py
	PYTHONPATH=. python huTools/unicode.py

coverage: dependencies
	printf '.*/tests/.*\n.*test.py\n' > .figleaf-exclude.txt
	printf '/usr/local/lib/.*\n/opt/.*\ntestenv/.*\n' >> .figleaf-exclude.txt
	printf '.*manage.py\n.*settings.py\n.*setup.py\n.*urls.py\n' >> .figleaf-exclude.txt
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
	virtualenv testenv
	pip -q install -E testenv -r requirements.txt

statistics:
	sloccount --wide --details huTools | tee sloccount.sc

upload: doc
	python setup.py build sdist bdist_egg
	rsync dist/* root@cybernetics.hudora.biz:/usr/local/www/apache22/data/nonpublic/eggs/
	rsync dist/* root@cybernetics.hudora.biz:/usr/local/www/apache22/data/dist/huTools/
	rsync -r --delete html root@cybernetics.hudora.biz:/usr/local/www/apache22/data/dist/huTools/

publish:
	python setup.py build sdist bdist_egg upload
	rsync dist/* root@cybernetics.hudora.biz:/usr/local/www/apache22/data/dist/huTools/
	rsync -r --delete html root@cybernetics.hudora.biz:/usr/local/www/apache22/data/dist/huTools/

doc:
	rm -Rf html
	mkdir -p html
	mkdir -p html/calendar
	sh -c '(cd html; pydoc -w ../huTools/*.py)'
	sh -c '(cd html/calendar; pydoc -w ../../huTools/calendar/*.py)'

install: build
	sudo python setup.py install


doc/standards/examples/%.xml: doc/standards/examples/%.json
	python huTools/protocols.py $<  | xmllint --encode utf-8 --format - > $@

examples: doc/standards/examples/warenzugang.xml doc/standards/examples/kommiauftrag.xml doc/standards/examples/rueckmeldung.xml doc/standards/examples/wms2logos_warenzugang.xslt doc/standards/examples/wms2logos_kommiauftrag.xslt
	xsltproc doc/standards/examples/wms2logos_warenzugang.xslt doc/standards/examples/warenzugang.xml > doc/standards/examples/wms2logos_warenzugang.xml
	xsltproc doc/standards/examples/wms2logos_kommiauftrag.xslt doc/standards/examples/kommiauftrag.xml > doc/standards/examples/wms2logos_kommiauftrag.xml


clean:
	rm -Rf testenv build dist html test.db pylint.out sloccount.sc pip-log.txt
	find . -name '*.pyc' -or -name '*.pyo' -delete

.PHONY: build clean install upload check
