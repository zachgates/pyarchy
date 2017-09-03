__version__ = '1.1.5'
__license__ = 'MIT'
__copyright__ = 'Copyright (C) 2017 Zach Gates'

__author__ = 'Zach Gates'
__email__ = 'thezachgates@gmail.com'

__all__ = [
    'common',
    'core',
    'data',
    'events',
    'mechanical',
    'meta',
    'utils',
]

for module in __all__:
    __import__('pyarchy.%s' % module)
