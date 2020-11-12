'''
Defines test cases for `requirements` models
'''


import json

from django.contrib.auth.models import User
from django.test import TestCase

from requirements import models


class UnitTests(TestCase):
    '''
    Defines test cases for the `Unit` model
    '''

    def test_model_saves_and_returns_special_characters_correctly_µ(self):
        '''
        `Unit` model should be able to save and return special characters without
        erroring or adding additional escape characters

        µA should be saved and returned correctly
        '''

        entry_data = json.loads(
            '{"name": "micro-amp", "name_plural": "micro-amps", "symbol": "µA", ' /
            '"description": "electric current"}'
        )

        entry = models.Unit.objects.create(**entry_data)

        # Confirm `Unit` str method returns the symbol correctly without modification
        self.assertEqual(str(entry), 'µA')


class TermTests(TestCase):
    '''
    Defines test cases for the `Term` model
    '''

    def setUp(self):
        '''
        Common setup for each test case
        '''

        # Create a user model for testing
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_entry_save_makes_boolean_true_condition_upper(self):
        '''
        `Term` model should make `boolean_true_condition` field string upper case

        If `boolean_true_condition` field is filled, make upper case on save
        '''

        # Create a `Term` entry
        entry = models.Term.objects.create(
            added_user=self.user, boolean_true_cond='my true', modified_user=self.user,
            name='my var'
        )

        # should have been made upper case on save
        self.assertEqual(entry.boolean_true_cond, 'MY TRUE')

    def test_entry_save_makes_boolean_false_condition_upper(self):
        '''
        `Term` model should make `boolean_false_condition` field string upper case

        If `boolean_false_condition` field is filled, make upper case on save
        '''

        # Create a `Term` entry
        entry = models.Term.objects.create(
            added_user=self.user, boolean_false_cond='my false', modified_user=self.user,
            name='my var'
        )

        # should have been made upper case on save
        self.assertEqual(entry.boolean_false_cond, 'MY FALSE')
