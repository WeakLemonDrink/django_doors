'''
Defines admin display for the `requirements` app
'''

from django.contrib import admin

from requirements.models import Unit


class UnitAdmin(admin.ModelAdmin):
    '''
    Defines admin display for the `unit` model
    '''

    list_display = ('symbol', 'name', 'description', 'is_active')


admin.site.register(Unit, UnitAdmin)
