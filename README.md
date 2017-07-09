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

 * No packaging boilerplate
 * Executable `.zip` file if module provides `main()` function
 * Command line script entry for the `main()` function
 * `requirements.txt` detected and included

#### Details

Necessary package fields are read from the .py module, without
imporing it:

  * `name` - extracted from the module filename
  * `__author__`
  * `__version__`
  * `__url__`

Also detects and inserts these optional fields:

  * `__license__`
  * `description` - first line of module docstring

Python packaging still relies on `setup.py`, so it is created
automatically.

`requirements.txt` should use safe setuptools subset
https://github.com/pypa/setuptools/issues/1080#issuecomment-313934637

`main()` function is required to enable *executable* features.

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
