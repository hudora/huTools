# Development at hudora

Here we store Information in regard to Software Development at Hudora.

## Tools

* We use [howsmycode.com][howsmycode] for code reviews. 
  ([Introduction][howsmycodeintro]) - you should create an account there
* We use [github.com/hudora][github] for version control
  ([Introduction][githubintro])  - you should create an account there
* We use [help.hudora.biz][tender] for support
  ([Introduction][tenderintro]) - you should create an account there
* We use [hudora.lighthouseapp.com][lighthouseapp] for feature requests
  ([Introduction][lighthousintro]) - you should create an account there
* [Textmate][textmatetips] is the offical Editor at Hudora Cybernetics.

[howsmycode]: http://howsmycode.com/
[howsmycodeintro]: https://cybernetics.hudora.biz/intern/wordpress/2009/12/howsmycode-erste-schritte/
[github]: http://github.com/hudora
[githubintro]: https://cybernetics.hudora.biz/intern/wordpress/2009/12/github-it-is/
[tender]: http://help.hudora.biz/
[tenderintro]: https://cybernetics.hudora.biz/intern/wordpress/2009/12/tender-it-is/
[lighthouseapp]: http://hudora.lighthouseapp.com
[lighthousintro]: https://cybernetics.hudora.biz/intern/wordpress/2009/12/lighthouse-it-is/
[textmatetips]: http://al3x.net/2008/12/03/how-i-use-textmate.html


##  Code

 * [Refactor Mercilessly][refactor] - your own code and others.
 * If you touch a file you are responsible that it is in decent shape afterwards. Even if it was messy 
   *before* you touched it.
 * Before ending the day, always check in.
 * Work in branches. For every feature/ticket create a branch. If the feature is taking more than a day
   to implement, create a fork. See [Ultimate Quality Development System][divmod] for an example how to work
   that way.
 * Check the [timeline/dashboard][timeline] regulary to see what's happening.
   Skimm the changesets and ask if you don't understand something.
 * always do `make test`, `make check` or equivalent before commit.

[refactor]: http://www.extremeprogramming.org/rules/refactor.html
[divmod]: http://divmod.org/trac/wiki/UltimateQualityDevelopmentSystem
[timeline]: https://github.com/


## Style

 * Wrap code at line 110. If you use Textmate type
   `defaults write com.macromates.textmate OakWrapColumns '( 40, 72, 78, 109 )'` to make wraping
   more comfortable.
 * Follow [PEP 8][pep8].
   Use [pep8.py][pep8py] `--ignore=E501,W291 --repeat` to verify compliance.
 * Follow [PEP 257][pep257] for docstrings
 * No tabs. Not anywhere. Always indent with 4 spaces.
 * Wrap at Column 109
 * Use [pylint][pylint]. aim for a score of at least 8. The higher the better. If you score is below 8
   be prepared to present a good reason for it.
 * Classes/Variables which reference Objects specific to our ERP/our Industry/german trade
   should be in german as technical terms. Generic Objects should be named in english: "Lieferscheinnummer",
   "Kundenauftragsnumer", "Rechnung" but "TransportEndpoint" and "DataStore". This line is very blurry.
   Comments in the code should be in english. See the "Protokolle" at SoftwareEntwicklung for further
   guidelines on naming.
 * Code should be targeted at Python 2.5 on FreeBSD / Ubuntu Linux
 * Functions should be no longer than a screen.
 * Helper functions should appear above their parent functions.
 * Let [the Zen of Python][zen] guide you.
 * [Fail Fast][failfast] and [crash early][crashearly]!
 * Write doctests. Write unittests. Aim for a [test coverage][coverage]
   of at least 80%. The higher the better.
 * `__underscore_methods__()` and inner classes should always be defined first within a class.

[pep8]: http://www.python.org/dev/peps/pep-0008/
[pep8py]: http://svn.browsershots.org/trunk/devtools/pep8/pep8.py
[pep257]: http://www.python.org/dev/peps/pep-0257/
[pylint]: http://www.python.org/pypi/pylint 
[zen]: http://www.python.org/dev/peps/pep-0020/
[failfast]: http://en.wikipedia.org/wiki/Fail-fast 
[crashearly]: https://cybernetics.hudora.biz/intern/wordpress/2008/11/offensive-programming-or-crash-early-crash-often/
[coverage]: http://www.python.org/pypi/coverage


## Conventions

http://github.com/hudora/huTools/blob/master/doc/standards/address_protocol.markdown
http://github.com/hudora/huTools/blob/master/doc/standards/messaging_ic-wms.markdown


## Django Specifica

* use `/cs/global_django_settings.py`
* your `settings.py` should be configured for testing
* you should provide a `settings_live.py` file. `settings.py` should be configured for testing
* including the directory `generic_templates` containing source:projects/html/trunk/templates
  ({{{svn co https://cybernetics.hudora.biz/intern/svn/code/projects/html/trunk/templates generic_templates}}})


## Misc

* you can assume that setuptools, virtualenv, pip and hudorakit are installed
* requirements have to be mentioned in requirements.txt and setup.py


## Required Reading

* [The Zen of Python][zen]
* [Code Like a Pythonista: Idiomatic Python][idiomatic]
* [Refactoring: Improving the Design of Existing Code][refactoring] by Fowler, Beck, Brant, Opdyke, Roberts
* [An Illustrated History of Failure][failure] (Video)
* [Developing reusable apps][reusable]

[zen]: http://www.python.org/dev/peps/pep-0020/
[idiomatic]: http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html
[refactoring]: http://www.pearsonhighered.com/academic/product/0,,0201485672,00%2Ben-USS_01DBC.html
[failure]: http://cybernetics.hudora.biz/nonpublic/Paul%20Fenwick,%20Perl%20Training%20Australia_%20_An%20Illustrated%20History%20of%20Failure_.mov
[reusable]: http://www.b-list.org/weblog/2008/mar/15/slides/
