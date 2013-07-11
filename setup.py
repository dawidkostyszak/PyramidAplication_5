import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'nokaut',
    'allegro'
    ]

dependency_list = [
    'https://github.com/dawidkostyszak/allegro/archive/master.tar.gz#egg=allegro',
    'https://github.com/dawidkostyszak/nokaut/archive/master.tar.gz#egg=nokaut'
]

setup(name='PyramidAplication',
        version='0.0',
        description='PyramidAplication',
        long_description=README + '\n\n' + CHANGES,
        classifiers=[
            "Programming Language :: Python",
            "Framework :: Pyramid",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
        author='',
        author_email='',
        url='',
        keywords='web wsgi bfg pylons pyramid',
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        test_suite='pyramidaplication',
        dependency_links=dependency_list,
        install_requires=requires,
        entry_points="""\
        [paste.app_factory]
        main = pyramidaplication:main
        [console_scripts]
        initialize_PyramidAplication_db = pyramidaplication.scripts.initializedb:main
        """,
)
