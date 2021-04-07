'''
Definition of data input forms for the `requirements` Django web app
'''


from django import forms

from requirements import models


class TermForm(forms.ModelForm):
    '''
    Form for the `Term` model
    '''

    def __init__(self, *args, **kwargs):
        '''
        Override superclass `__init__` to save incoming `request.user`
        '''

        # If current_user is in kwargs, pop out and save to class
        self.current_user = kwargs.pop('current_user', None)

        # Call superclass init
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.Term
        fields = ['name', 'd_type', 't_type', 'description', 'value', 'units', 'max_value',
                  'min_value', 'boolean_false_cond', 'boolean_true_cond']

    def clean(self):
        '''
        Override superclass `clean()` to:
         * Add `added_user` and `modified_user`
         * If `d_type` is `BOOLEAN`, both `boolean_false_cond` and `boolean_true_cond` should be
           filled
         * If `t_type` is `CONSTANT`, `value` should be filled
        '''

        cleaned_data = super().clean()

        if self.current_user:
            cleaned_data['added_user'] = self.current_user
            cleaned_data['modified_user'] = self.current_user

        if cleaned_data['d_type'] == models.Term.BOOLEAN:
            if not cleaned_data['boolean_false_cond']:
                self.add_error('boolean_false_cond', 'This field should be filled.')

            if not cleaned_data['boolean_true_cond']:
                self.add_error('boolean_true_cond', 'This field should be filled.')

        if cleaned_data['t_type'] == models.Term.CONSTANT:
            if not cleaned_data['value']:
                self.add_error('value', 'This field should be filled.')

        return cleaned_data
