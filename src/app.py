import glob
import os
import sys
import unittest

import click
import coverage
from project import create_app, db

if os.environ.get('FLASK_ENV') == 'development':
    COV = coverage.coverage(
        branch=True,
        include=[
            'project/*',
        ],
        omit=[
            'project/*/tests/*',
            'project/_tests/*',
            'project/__init__.py',
        ]
    )
    COV.start()

app = create_app()

paths = [
    'project/heartbeat/tests'
]


@app.cli.command()
@click.option('--file', default=None)
def test(file: str) -> None:
    """Runs the tests without code coverage."""
    for path in paths:
        tests = unittest.TestSuite()
        if file is None:
            tests = unittest.TestLoader().discover(
                path, pattern='test_*.py')
        else:
            tests = unittest.TestLoader().discover(
                path, pattern=f'test_{file}.py')
        result = unittest.TextTestRunner(verbosity=2).run(tests)
        if result.wasSuccessful():
            continue
        sys.exit(1)
    sys.exit(0)


@app.cli.command()
def cov() -> None:
    """Runs the unit tests with coverage."""
    try:
        COV
    except NameError:
        raise Exception('''
            No coverage data collected.
            You may need to set environment variable FLASK_ENV=development
        ''')
    for path in paths:
        tests = unittest.TestLoader().discover(path)
        result = unittest.TextTestRunner(verbosity=0).run(tests)
        if result.wasSuccessful():
            COV.stop()
            COV.save()
            print('Coverage Summary:')
            COV.report()
            COV.html_report()
            COV.erase()
            sys.exit(0)
        sys.exit(1)


def run_migration() -> None:
    if os.environ.get('FLASK_ENV') != 'development':
        sys.exit(1)
    for file in glob.glob('/tables/*'):
        with open(file) as table:
            query = table.read()
            db.session.execute(query)
            db.session.commit()


@app.cli.command()
def migrate() -> None:
    """Runs migration for database."""
    run_migration()


if __name__ == '__main__':
    app.cli()
