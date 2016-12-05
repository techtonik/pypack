Packs .py module into executable .zip source distribution.

No extra files required - necessary package fields are read
from the .py module, without imporing it:

  * `name` - extracted from the module filename
  * `__author__`
  * `__version__`
  * `__url__`

Also detects and inserts these optional fields:

  * `__license__`
  * `description` - first line of module docstring

No `setup.py` is needed. Resulting `.zip` file is
**executable**, so make sure the module exports `main()`
function.


##### Usage

* [ ] Pack your module into .zip archive

        pypack.py <module.py>

* [ ] Write changelog

* [ ] Upload archive to PyPI (manually for now)
  * [ ] Create new version https://pypi.python.org/pypi?%3Aaction=submit_form&name=<module>
  * [ ] Upload .zip for this version

* [ ] Update PyPI description (also manual process)
  * [ ] Download PKG-INFO
  * [ ] Edit and upload

* [ ] Tag release

    ```
    git tag -a
    git push --follow-tags
    ```
