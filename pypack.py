#!/usr/bin/env python
"""
Wrap Python module into executable .zip package.

Extracts required meta-data (author|maintainer, name, version,
url) and optional fields (description) from module without
importing it.

  * [x] name, version
  * [x] author
  * [x] license
  * [x] url
  * [x] description (first line of module docstring)

Features:

  * [x] make .zip executable if main() is defined
  * [x] generate executable script if main() is found

Public domain work by:
  anatoly techtonik <techtonik@gmail.com>
"""

__version__ = '0.2dev'

import os
import sys

def get_field(path, name='__version__'):
  '''Read named string from module without importing it'''
  for line in open(path, 'rb'):
    # Decode to unicode for PY2/PY3 in a fail-safe way
    line = line.decode('cp437')
    if line.startswith(name):
      # __version__ = "0.9"
      delim = '\"' if '\"' in line else '\''
      return line.split(delim)[1]

def get_description(path):
  '''Return first non-empty line from module docstring'''
  mf = open(path, 'rb')
  for i, line in enumerate(mf):
    if i > 10:
      # stop looking after 10 lines
      break
    line = line.decode('utf-8').strip()
    if '"""' in line or "'''" in line:
      while line.strip('\n\t\r \'\"') == '':
        line = next(mf)
        line = line.decode('utf-8').strip()
      return line

def get_main(path):
  '''Return True if module defines main() function'''
  with open(path, 'rb') as mf:
    for line in mf:
      if line.startswith('def main('):
        return True


def zipadd(archive, filename, newname):
  '''Add filename to archive. `newname` is required. Otherwise
     zipfile may create unsafe entries, such as "../patch.py".
     Returns open ZipFile object.
  '''
  import zipfile
  zf = zipfile.ZipFile(archive, 'a', zipfile.ZIP_DEFLATED)
  zf.write(filename, newname)
  return zf

class MiniJinja(object):
    """Template engine that knows how to render {{ tag }}"""

    def __init__(self, templates='.'):
        """templates  - template path"""
        import re
        import sys
        self.PY3K = sys.version_info[0] == 3

        self.path = templates + '/'
        self.tag  = re.compile('{{ *(?P<tag>\w+) *}}')

    def render(self, tplfile, vardict=None, **kwargs):
        """returns unicode str"""
        tpltext = open(self.path + tplfile).read()
        return self.render_string(tpltext, vardict, **kwargs)

    def render_string(self, tpltext, vardict=None, **kwargs):
        data = vardict or {}
        data.update(kwargs)

        def lookup(match):
            return data[match.group('tag')]

        if not self.PY3K:
            return unicode(self.tag.sub(lookup, tpltext))
        else:
            return self.tag.sub(lookup, tpltext)

# ---

BASE = os.path.abspath(os.path.dirname(__file__))

MAINTPL = """\
import sys

import {{ module }}
sys.exit({{ module }}.main())
"""

SETUPTPL = """\
from distutils.core import setup

setup(
    name='{{ module }}',
    version='{{ version }}',
    author='{{ author }}',
    url='{{ url }}',

    description='{{ description }}',
    license='{{ license }}',

    py_modules=['{{ module }}'],

    entry_points = {
        'console_scripts': ['{{ executable }}'],
    },

    classifiers=[
        'Classifier: Programming Language :: Python :: 2',
        'Classifier: Programming Language :: Python :: 3',
    ],
)
"""

def main():
  if not sys.argv[1:]:
    sys.exit("usage: pack.py <module.py>")

  modpath = sys.argv[1]
  modname = os.path.basename(modpath)[:-3]  # and strip extension
  tplvars = dict(
    module = modname,
    version = get_field(modpath, '__version__'),
    author = get_field(modpath, '__author__'),
    license = get_field(modpath, '__license__'),
    url = get_field(modpath, '__url__'),
    description = get_description(modpath),

    executable = ''
  )

  if tplvars['version'] == None:
    sys.exit("error: no __version__ specifier found in %s" % modpath)
  if tplvars['author'] == None:
    sys.exit("error: no __author__ specifier found in %s" % modpath)
  packname = tplvars['module'] + "-" + tplvars['version'] + ".zip"
  print("[*] Packing %s into %s" % (modpath, packname))
  if os.path.exists(packname):
    os.remove(packname)
  zf = zipadd(packname, modpath, os.path.basename(modpath))
  if not get_main(modpath):
     print("[*] main() not found, not making executable")
  else:  
     print("[*] Making %s executable" % (packname))
     # http://techtonik.rainforce.org/2015/01/shipping-python-tools-in-executable-zip.html
     text = MiniJinja(BASE).render_string(MAINTPL, **tplvars)
     zf.writestr('__main__.py', text)
     tplvars['executable'] = '%s=%s:main' % (modname, modname)
  print("[*] Making %s installable" % (packname))
  text2 = MiniJinja(BASE).render_string(SETUPTPL, **tplvars)
  zf.writestr('setup.py', text2)
  print("[*] Making %s uploadable to PyPI" % (packname))
  zf.writestr('PKG-INFO', '')
  zf.close()

if __name__ == '__main__':
  main()
