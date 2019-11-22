# services/users/manage.py


import sys
import unittest

from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models.users import UserModel

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)


@cli.command('seed_db')
def seed_db():
    """Seeds the database."""
    db.session.add(UserModel(username='argi', email="argipapaefstathiou@gmail.com", password="supplyit"))
    db.session.add(UserModel(username='jimbill', email="dimitrakisvasilis@gmail.com", password="supplyit"))
    db.session.commit()


if __name__ == '__main__':
    cli()
