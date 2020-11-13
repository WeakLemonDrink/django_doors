'''
Defines admin display for the `requirements` app
'''

from django.contrib import admin

from reversion.admin import VersionAdmin

from requirements import forms, models


@admin.register(models.Component)
class ComponentAdmin(VersionAdmin):
    '''
    Defines admin display for the `component` model

    Implements `django-reversion` functionality
    '''


@admin.register(models.Unit)
class UnitAdmin(admin.ModelAdmin):
    '''
    Defines admin display for the `unit` model
    '''

    list_display = ('symbol', 'name', 'description', 'is_active')


@admin.register(models.Term)
class TermAdmin(VersionAdmin):
    '''
    Defines admin display for the `Term` model

    Implements `django-reversion` functionality
    '''

    form = forms.TermForm
