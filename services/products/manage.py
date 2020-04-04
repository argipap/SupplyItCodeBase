# manage.py


import sys
import unittest

import coverage
from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models.product_categories import ProductCategoryModel
from project.api.models.products import ProductModel


COV = coverage.coverage(
    branch=True, include="project/*", omit=["project/tests/*", "project/config.py",]
)
COV.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover("project/tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover("project/tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print("Coverage Summary:")
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    sys.exit(result)


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_categories")
def seed_categories():
    """Seeds the product_categories table in database."""
    product_categories = [
        "meat_and_poultry",
        "dairy_and_eggs",
        "alcohol_and_beverages",
        "food_and_vegetables",
        "seafood",
    ]
    for category_name in product_categories:
        ProductCategoryModel(name=category_name).save_to_db()


@cli.command("seed_products")
def seed_products():
    """Seeds the products table in database."""
    ProductModel(
        name="JOSE CUERVO RESERVA 1800 ANEJO 700ml",
        code="24.053",
        category_id=ProductCategoryModel.get_category_id_by_name(
            category_name="alcohol_and_beverages"
        ),
    ).save_to_db()


if __name__ == "__main__":
    cli()
