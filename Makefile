# setting the PATH seems only to work in GNUmake not in BSDmake
PATH := ./testenv/bin:$(PATH)

default: dependencies check test statistics

check:
	find huTools -name '*.py' | xargs /usr/local/hudorakit/bin/hd_pep8
	/usr/local/hudorakit/bin/hd_pylint huTools | tee pylint.out

build:
	python setup.py build

dependencies:
	virtualenv testenv
	pip -q install -E testenv -r requirements.txt

statistics:
	sloccount --wide --details . | grep -v -E '(testenv|build)' > sloccount.sc

upload: doc
	python setup.py build sdist bdist_egg
	rsync dist/* root@cybernetics.hudora.biz:/usr/local/www/apache22/data/dist/huTools/
	rsync -r --delete html root@cybernetics.hudora.biz:/usr/local/www/apache22/data/dist/huTools/

publish:
	# remove development tag
	perl -npe 's/^tag_build = .dev/# tag_build = .dev/' -i setup.cfg
	svn commit -m "release of echo `grep version setup.py`"
	python setup.py build sdist bdist_egg upload
	rsync dist/* root@cybernetics.hudora.biz:/usr/local/www/apache22/data/dist/huTools/
	rsync -r --delete html root@cybernetics.hudora.biz:/usr/local/www/apache22/data/dist/huTools/
	# add development tag
	perl -npe 's/^\# tag_build = .dev/tag_build = .dev/' -i setup.cfg
	rsync dist/* root@cybernetics.hudora.biz:/usr/local/www/apache22/data/dist/huTools/
	echo "now bump version number in setup.py and commit"

doc:
	rm -Rf html
	mkdir -p html
	mkdir -p html/calendar
	sh -c '(cd html; pydoc -w ../huTools/*.py)'
	sh -c '(cd html/calendar; pydoc -w ../../huTools/calendar/*.py)'

test:
	PYTHONPATH=. python huTools/humessaging.py
	PYTHONPATH=. python huTools/luids.py
	PYTHONPATH=. python huTools/checksumming.py
	PYTHONPATH=. python huTools/calendar/workdays.py
	PYTHONPATH=. python huTools/calendar/formats.py
	PYTHONPATH=. python huTools/unicode.py

install: build
	sudo python setup.py install

clean:
	rm -Rf testenv build dist html test.db pylint.out sloccount.sc
	find . -name '*.pyc' -or -name '*.pyo' -delete

.PHONY: build clean install upload check
