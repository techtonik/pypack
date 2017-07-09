No boilerplate way to create executable source package for Python module.

```
$ python -m pypack appvey.py
[*] Packing appvey.py into appvey-1234.zip
[*] Making appvey-1234.zip executable
[*] Making appvey-1234.zip installable
[*] Making appvey-1234.zip uploadable to PyPI
```

**See also**:
* https://github.com/takluyver/flit
* http://ccpgames.github.io/pypackage/

#### Features

No extra files required - necessary package fields are read
from the .py module, without imporing it:

  * `name` - extracted from the module filename
  * `__author__`
  * `__version__`
  * `__url__`

Also detects and inserts these optional fields:

  * `__license__`
  * `description` - first line of module docstring

`setup.py` is not needed (it is created automatically when
creating archive, because Python still requires it). Resulting
`.zip` file is **executable**, so make sure the module exports
`main()` function.


##### Checklist for packaging your module for PyPI

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
