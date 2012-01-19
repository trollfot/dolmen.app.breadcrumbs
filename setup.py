from setuptools import setup, find_packages
from os.path import join

name = 'dolmen.app.breadcrumbs'
version = '2.0'
readme = open(join('src', 'dolmen', 'app', 'breadcrumbs', 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'cromlech.browser >= 0.4',
    'cromlech.io',
    'dolmen.location >= 0.1',
    'dolmen.template',
    'dolmen.viewlet',
    'grokcore.component',
    'setuptools',
    'zope.dublincore',
    'zope.interface',
    ]

tests_require = [
    'cromlech.browser [test]',
    'zope.location',
    ]

setup(name = name,
      version = version,
      description = 'Breadcrumbs navigation for Dolmen applications.',
      long_description = readme + '\n\n' + history,
      keywords = 'Grok Zope3 CMS Dolmen',
      author = 'Souheil Chelfouh',
      author_email = 'trollfot@gmail.com',
      url = 'http://gitweb.dolmen-project.org',
      download_url = '',
      license = 'ZPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages = ['dolmen', 'dolmen.app'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      tests_require = tests_require,
      install_requires = install_requires,
      extras_require = {'test': tests_require},
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: Zope Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
      ],
      )
