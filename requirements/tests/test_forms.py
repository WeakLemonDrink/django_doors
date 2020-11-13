'''
Defines test cases for `requirements` forms
'''


from django.contrib.auth.models import User
from django.test import TestCase

from requirements import forms, models


class TermFormTests(TestCase):
    '''
    Defines test cases for the `TermForm` form
    '''

    def setUp(self):
        '''
        Common setup for each test case
        '''

        # Create a user model for testing
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_init_saves_user_to_class(self):
        '''
        `TermForm` should save input user to class if supplied on init
        '''

        form = forms.TermForm(current_user=self.user)

        # Confirm user has been saved to form
        self.assertEqual(form.current_user, self.user)

    def test_is_valid_true_default_data(self):
        '''
        `TermForm` `is_valid()` should return true if valid data is supplied

        `added_user`, `d_type`, `t_type`, `modified_user` and `name` are minimum fields required
        to create a new `Term` entry
        '''

        post_data = {
            'added_user': self.user, 'd_type': models.Term.NONE, 't_type': models.Term.DEFINITION,
            'modified_user': self.user, 'name': 'my var'
        }

        form = forms.TermForm(post_data)

        # Should return true as supplied with minimum data required to create an entry
        self.assertTrue(form.is_valid())

    def test_is_valid_true_without_user_data(self):
        '''
        `TermForm` `is_valid()` should return true if valid data is supplied

        If `added_user` and `modified_user` are not supplied in the post data, this data can be
        supplied via the `current_user` kwarg on init
        '''

        post_data = {
            'd_type': models.Term.NONE, 't_type': models.Term.DEFINITION, 'name': 'my var'
        }

        form = forms.TermForm(post_data, current_user=self.user)

        # Should return true as supplied with minimum data required to create an entry
        self.assertTrue(form.is_valid())

    def test_clean_includes_added_user(self):
        '''
        `TermForm` overridden clean method should add `added_user` to the cleaned data, so valid
        data is supplied
        '''

        post_data = {
            'd_type': models.Term.NONE, 't_type': models.Term.DEFINITION, 'name': 'my var'
        }

        form = forms.TermForm(post_data, current_user=self.user)

        # call is_valid which in turn calls clean
        form.is_valid()

        # Confirm the cleaned data contains `added_user`
        self.assertEqual(form.cleaned_data['added_user'], self.user)

    def test_clean_includes_modified_user(self):
        '''
        `TermForm` overridden clean method should add `modified_user` to the cleaned data, so valid
        data is supplied
        '''

        post_data = {
            'd_type': models.Term.NONE, 't_type': models.Term.DEFINITION, 'name': 'my var'
        }

        form = forms.TermForm(post_data, current_user=self.user)

        # call is_valid which in turn calls clean
        form.is_valid()

        # Confirm the cleaned data contains `modified_user`
        self.assertEqual(form.cleaned_data['modified_user'], self.user)

    def test_d_type_boolean_conditions_filled_is_valid_true(self):
        '''
        `TermForm` should return `is_valid` == `True` for valid data combinations

        If data type is BOOLEAN, both `boolean_true_cond` and `boolean_false_cond` should be
        filled. If this condition is met, data is valid
        '''

        post_data = {
            'boolean_false_cond': 'FALSE', 'boolean_true_cond': 'TRUE',
            'd_type': models.Term.BOOLEAN, 't_type': models.Term.DEFINITION, 'name': 'my var'
        }

        form = forms.TermForm(post_data, current_user=self.user)

        # Should return true as supplied with valid data
        self.assertTrue(form.is_valid())

    def test_d_type_boolean_boolean_false_cond_blank_is_valid_false(self):
        '''
        `TermForm` should return `is_valid` == `False` for invalid data combinations

        If data type is BOOLEAN, both `boolean_true_cond` and `boolean_false_cond` should be
        filled. If `boolean_false_cond` is not filled, data is not valid
        '''

        post_data = {
            'boolean_false_cond': None, 'boolean_true_cond': 'TRUE',
            'd_type': models.Term.BOOLEAN, 't_type': models.Term.DEFINITION, 'name': 'my var'
        }

        form = forms.TermForm(post_data, current_user=self.user)

        # Should return false as supplied with invalid data
        self.assertFalse(form.is_valid())

    def test_d_type_boolean_boolean_false_cond_blank_raise_error(self):
        '''
        `TermForm` should raise errors for invalid data combinations

        If data type is BOOLEAN, both `boolean_true_cond` and `boolean_false_cond` should be
        filled. If `boolean_false_cond` is not filled, data is not valid
        '''

        post_data = {
            'boolean_false_cond': None, 'boolean_true_cond': 'TRUE',
            'd_type': models.Term.BOOLEAN, 't_type': models.Term.DEFINITION, 'name': 'my var'
        }

        form = forms.TermForm(post_data, current_user=self.user)

        # Should return error attached to `boolean_false_cond` field
        self.assertEqual(form.errors['boolean_false_cond'], ['This field should be filled.'])

    def test_d_type_boolean_boolean_true_cond_blank_is_valid_false(self):
        '''
        `TermForm` should return `is_valid` == `False` for invalid data combinations

        If data type is BOOLEAN, both `boolean_true_cond` and `boolean_false_cond` should be
        filled. If `boolean_true_cond` is not filled, data is not valid
        '''

        post_data = {
            'boolean_false_cond': 'FALSE', 'boolean_true_cond': None,
            'd_type': models.Term.BOOLEAN, 't_type': models.Term.DEFINITION, 'name': 'my var'
        }

        form = forms.TermForm(post_data, current_user=self.user)

        # Should return false as supplied with invalid data
        self.assertFalse(form.is_valid())

    def test_d_type_boolean_boolean_true_cond_blank_raise_error(self):
        '''
        `TermForm` should raise errors for invalid data combinations

        If data type is BOOLEAN, both `boolean_true_cond` and `boolean_false_cond` should be
        filled. If `boolean_true_cond` is not filled, data is not valid
        '''

        post_data = {
            'boolean_false_cond': 'FALSE', 'boolean_true_cond': None,
            'd_type': models.Term.BOOLEAN, 't_type': models.Term.DEFINITION, 'name': 'my var'
        }

        form = forms.TermForm(post_data, current_user=self.user)

        # Should return error attached to `boolean_true_cond` field
        self.assertEqual(form.errors['boolean_true_cond'], ['This field should be filled.'])
