try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


config = {
    'name'             : 'Redis Grepper',
    'description'      : 'Perform regex searches through Redis values',
    'author'           : 'Ionut G. Stan',
    'author_email'     : 'ionut.g.stan@gmail.com',
    'url'              : 'http://github.com/igstan/regis-grep',
    'download_url'     : 'http://github.com/igstan/redis-grep/archives/0.1.0',
    'version'          : '0.1.0',
    'install_requires' : ['redis'],
    'py_modules'       : ['redisgrep'],
    'scripts'          : ['redis-grep'],
}

setup(**config)
