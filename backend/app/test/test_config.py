"""Backend test configuration"""
import os
import unittest
from flask import current_app
from flask_testing import TestCase
from app import app
from app.main.config import basedir

class TestDevelopmentConfig(TestCase):
    """Tests the development configuration"""
    def create_app(self):
        """Create an app for development"""
        app.config.from_object('app.main.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        """Check if the app is in development"""
        self.assertFalse(app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        uri = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db')
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == uri
        )


class TestTestingConfig(TestCase):
    """Tests the testing configuration"""
    def create_app(self):
        """Create an App for test"""
        app.config.from_object('app.main.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        """Check if the app is in test"""
        self.assertFalse(app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(app.config['DEBUG'])
        uri = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == uri
        )


class TestProductionConfig(TestCase):
    """Tests the production configuration"""
    def create_app(self):
        """Create an app for production"""
        app.config.from_object('app.main.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        """Check if the app is in production"""
        self.assertTrue(app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()
