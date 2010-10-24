# Development at Hudora

Here we store Information in regard to Software Development at Hudora.

## Tools


* We use [github.com/hudora][github] for version control
  ([Introduction][githubintro])  - you should create an account there
* [Textmate][textmatetips] is the offical editor at Hudora Cybernetics. Use the `PyBicicle Repair Man`
  and `Python PEP8` Plugins.

[github]: http://github.com/hudora
[githubintro]: https://cybernetics.hudora.biz/intern/wordpress/2009/12/github-it-is/
[textmatetips]: http://al3x.net/2008/12/03/how-i-use-textmate.html


##  Coding

 * [Refactor Mercilessly][refactor] - your own code and others.
 * If you touch a file you are responsible that it is in decent shape afterwards. Even if it was messy 
   *before* you touched it.
 * Before ending the day, always check in and push to our central repository.
 * Your commit messages should be in english, use markdown and follow general
   [commit message best practices][commitmessage].
 * Check the [timeline/dashboard][timeline] regulary to see what's happening.
   Skimm the changesets and ask if you don't understand something.
 * always do `make test`, `make check` or equivalent before commit.
 * add the URL of the ticket in the ticket system to the end of your commit message
 * Work in branches where appropriate. For every feature/ticket a branch may be appropriate.

[refactor]: http://www.extremeprogramming.org/rules/refactor.html
[commitmessage]: http://www.tpope.net/node/106
[timeline]: https://github.com/


## Style

 * Wrap code at column 109. If you use Textmate type
   `defaults write com.macromates.textmate OakWrapColumns '( 40, 72, 78, 109 )'` to make wraping
   more comfortable.
 * Follow [PEP 8][pep8].
   Use [pep8.py][pep8py] `--ignore=E501,W291 --repeat` to verify compliance.
 * Follow [PEP 257][pep257] for docstrings
 * No tabs. Not anywhere (except in Makefiles). Always indent with 4 spaces.
 * Use [pylint][pylint]. Aim for a score of at least 8. The higher the better. If you score is below 8
   be prepared to present a good reason for it.
 * Classes/Variables which reference Objects specific to our ERP/our Industry/german trade
   should be in german as technical terms. Generic Objects should be named in english: "Lieferscheinnummer",
   "Kundenauftragsnumer", "Rechnung" but "TransportEndpoint" and "DataStore". This line is very blurry.
   Comments in the code should be in english. See the "Protokolle" at SoftwareEntwicklung for further
   guidelines on naming.
 * Variable Names should not be abbreviated. The only exceptions are "nummer" -> "nr" and
   "kommissionier" -> "kommi".
 * Code should be targeted at Python 2.5 on FreeBSD / Ubuntu Linux
 * Functions should be no longer than a screen.
 * Helper functions should appear above their parent functions.
 * `__underscore_methods__()` and inner classes should always be defined first within a class.
 * Let [the Zen of Python][zen] guide you and avoid [Anti-Idioms][donts].
 * [Fail Fast][failfast] and [crash early][crashearly]!
 * Make your stuff [Idempotent][idempotent].
 * avoid float values where possible. They [probably don't work as you think they work][floats]. Store
   Cent instead of Euro, Millimeters instead of Centimeters and so on.
 * Write doctests. Write unittests. Aim for a [test coverage][coverage]
   of at least 80%. The higher the better.
 * Provide a `Makefile` with `dependencies`, `test` and `check` (pylint/pep8) targets.

[pep8]: http://www.python.org/dev/peps/pep-0008/
[pep8py]: http://svn.browsershots.org/trunk/devtools/pep8/pep8.py
[pep257]: http://www.python.org/dev/peps/pep-0257/
[pylint]: http://www.python.org/pypi/pylint 
[zen]: http://www.python.org/dev/peps/pep-0020/
[donts]: http://docs.python.org/howto/doanddont.html
[failfast]: http://en.wikipedia.org/wiki/Fail-fast 
[crashearly]: https://cybernetics.hudora.biz/intern/wordpress/2008/11/offensive-programming-or-crash-early-crash-often/
[coverage]: http://www.python.org/pypi/coverage
[floats]: http://docs.sun.com/source/806-3568/ncg_goldberg.html
[idempotent]: http://en.wikipedia.org/wiki/Idempotent

## Conventions

Use our naming conventions for [Adresses][adressprot], [Orders][orderprotocol] and
[Warehouse related stuff][icwmsprot] (more to come).

[adressprot]: http://github.com/hudora/huTools/blob/master/doc/standards/address_protocol.markdown
[orderprotocol]: http://github.com/hudora/huTools/blob/master/doc/standards/verysimpleorderprotocol.markdown
[icwmsprot]: http://github.com/hudora/huTools/blob/master/doc/standards/messaging_ic-wms.markdown


## Identifiers

Use global unique identifiers where ever possible. `huTools.luids.guid128()` creates somewhat compact representations of random IDs. It's even better if you can find an standartisized Scheme of unique IDs. Good Candidates are found in the [EPC Tag Data Standard (TDS)][tds], in [Tag URIs][taguri] as defined in [RfC 4151][rfc4151].

[tds]: http://www.epcglobalinc.org/standards/tds/
[taguri]: http://en.wikipedia.org/wiki/Tag_URI
[rfc4151]: http://tools.ietf.org/html/rfc4151


## Misc

* you can assume that setuptools, virtualenv, and pip are installed
* requirements have to be mentioned in `requirements.txt` and `setup.py`
* Always test Iñtërnâtiônàlizætiøn by putting strange strings into input fields
* Always test `<script>alert("XSS");</script> & <bold>Co</bold>` by putting strange strings into input fields
* use [huTools](http://hudora.github.com/huTools/) where appropriate
* `Iñtërnâtiônàlizætiøn <script>alert("XSS");</script> %+'"<!--` might be a goot test string.

## Django Specifica

* Target [Django 1.1.1][django]
* make extensive use of the [Django Admin][djangoadmin]
* [hd_django_project_template][hd_django_project_template] codifies our current best practices to structure
  a project.
* use [`cs.global_django_settings.py`][global_django_settings] (internal use only).
* including the directory `generic_templates` containing git@github.com:hudora/html.git
  (`git clone git@github.com:hudora/html.git html;ln -s html/templates generic_templates`) (internal use only)
* Use [googleappsauth][googleappsauth] to authenticate local users ([example][googleappsauthexample])

[django]: http://www.djangoproject.com/
[djangoadmin]: http://docs.djangoproject.com/en/1.1/ref/contrib/admin/
[hd_django_project_template]: http://github.com/hudora/hd_django_project_template
[global_django_settings]: https://github.com/hudora/CentralServices/blob/master/cs/global_django_settings.py
[googleappsauth]: http://github.com/hudora/django-googleappsauth#readme
[googleappsauthexample]: https://cybernetics.hudora.biz/intern/wordpress/2010/01/django-googleappsauth/
[hoptoad]: https://hudora.hoptoadapp.com/
[hoptoadexample]: https://cybernetics.hudora.biz/intern/wordpress/2010/01/hoptoad/
[silverlining]: http://cloudsilverlining.org/


### Django Models

Django Models always should come with `created_at` and `updated_at` fields. They also should use a Field
called `designator` as ther primary means of reference. If the designator is meant for human consumption it
should consist of a two letter Prefix unique for that model, a secquence number and a check digit. If the
designator is not (or seldom) for human consumption it should be a random unique value frefixed by two
letters. See https://cybernetics.hudora.biz/intern/trac/wiki/NummernKreise prefixes used so far.


    class Task(models.Model):
        id = models.AutoField(primary_key=True)
        designator = models.CharField(max_length=32, default='', blank=True, editable=False, db_index=True,
            unique=True)
        created_at = models.DateField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
    
    def _task_post_save_cb(signal, sender, instance, **kwargs):
        if not instance.designator:
            chash = hashlib.md5("%f-%f-%d" % (random.random(), time.time(), instance.id))
            instance.designator = "TC%s" % base64.b32encode(chash.digest()).rstrip('=')
            # instance.designator = huTools.checksumming.build_verhoeff_id("TC", instance.id)
            instance.save()
    models.signals.post_save.connect(_task_post_save_cb, Task)

Alternatively use a `guid` field. `huToos.luids.guid128()` can provide you with a decent value.


## Tools for internal Developers

* We use [hudora.lighthouseapp.com][lighthouseapp] for feature requests
  ([Introduction][lighthousintro]) - you should create an account there
[lighthouseapp]: http://hudora.lighthouseapp.com
[lighthousintro]: https://cybernetics.hudora.biz/intern/wordpress/2009/12/lighthouse-it-is/


## Required Reading

* [The Zen of Python][zen]
* [Code Like a Pythonista: Idiomatic Python][idiomatic]
* [Google Python Style Guide][pyguide]
* [Refactoring: Improving the Design of Existing Code][refactoring] by Fowler, Beck, Brant, Opdyke, Roberts
* [An Illustrated History of Failure][failure] (Video)
* [Getting unicode right in Python][unicode]
* [Developing reusable apps][reusable]

[zen]: http://www.python.org/dev/peps/pep-0020/
[idiomatic]: http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html
[pyguide]: http://google-styleguide.googlecode.com/svn/trunk/pyguide.html
[refactoring]: http://www.pearsonhighered.com/academic/product/0,,0201485672,00%2Ben-USS_01DBC.html
[failure]: http://cybernetics.hudora.biz/nonpublic/Paul%20Fenwick,%20Perl%20Training%20Australia_%20_An%20Illustrated%20History%20of%20Failure_.mov
[unicode]: http://blog.notdot.net/2010/07/Getting-unicode-right-in-Python
[reusable]: http://www.b-list.org/weblog/2008/mar/15/slides/

