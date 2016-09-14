Quickly pack .py module into source distribution.

Features:

* no `setup.py` is needed
* resulting `.zip` file is **executable**

Usage:

* [ ] Pack .zip archive

    pypack.py <module.py>

* [ ] Write changelog

* [ ] Upload archive to PyPI (manually for now)
  * [ ] Create new version https://pypi.python.org/pypi?%3Aaction=submit_form&name=<module>
  * [ ] Upload .zip for this version

* [ ] Update PyPI description (also manual process)
  * [ ] Download PKG-INFO
  * [ ] Edit and upload

* [ ] Tag release

    git tag -a
    git push --follow-tags
