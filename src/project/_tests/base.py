from app import run_migration
from flask import current_app as app
from flask_testing import TestCase
from project import db


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('project.configs.TestingConfig')
        return app

    def setUp(self):
        run_migration()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def assert201(self, response):
        self.assert_status(response, 201)
