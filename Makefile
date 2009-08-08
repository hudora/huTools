default: check test

check:
	find huTools -name '*.py'  -exec pep8 --ignore=E501,W291 --repeat {} \;
	pylint huTools

build:
	python setup.py build

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
	python huTools/humessaging.py
	python huTools/unicode.py
	python huTools/luids.py
	python huTools/checksumming.py
	python huTools/calendar/workdays.py
	python huTools/calendar/formats.py

install: build
	sudo python setup.py install

clean:
	rm -Rf build dist html test.db
	find . -name '*.pyc' -or -name '*.pyo' -delete

.PHONY: build clean install upload check
