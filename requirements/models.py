'''
Definition of database models for the `requirements` app
'''


from django.contrib.auth.models import User
from django.db import models

import reversion


class CoreModel(models.Model):
    '''
    Abstract base class

    Allows us to inherit common fields across different models
    '''

    added_date = models.DateTimeField('Date Added', auto_now_add=True)
    added_user = models.ForeignKey(
        User, related_name='%(app_label)s_%(class)s_added',
        on_delete=models.CASCADE)
    modified_date = models.DateTimeField('Last Modified', auto_now=True)
    modified_user = models.ForeignKey(
        User, related_name='%(app_label)s_%(class)s_modified',
        on_delete=models.CASCADE)
    removed = models.BooleanField(default=False)

    class Meta:
        abstract = True


@reversion.register()
class Component(CoreModel):
    '''
    Defines database table structure for `Component` entries

    Different components allow us to categorise system requirements
    '''

    name = models.CharField(max_length=140, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'requirements'
        ordering = ['name']

    def __str__(self):
        return self.name


class Unit(models.Model):
    '''
    Defines database table structure for `Unit` entries

    List of SI units to use with `Term` entries to ensure consistent units are used
    across the project
    '''

    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=140, unique=True)
    name_plural = models.CharField(max_length=140, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = 'requirements'
        ordering = ['name']

    def __str__(self):
        return self.symbol


@reversion.register()
class Term(CoreModel):
    '''
    Defines database table structure for `Term` entries

    Allows different terms to be used across the project, to form a data dictionary or
    interface control document
    '''

    # Data type choices
    NONE = 0
    BOOLEAN = 1
    ENUM = 2
    FLOAT = 3
    INTEGER = 4
    STRING = 5

    D_TYPE_CHOICES = (
        (NONE, 'None'),
        (BOOLEAN, 'Boolean'),
        (ENUM, 'Enumeration'),
        (FLOAT, 'Float'),
        (INTEGER, 'Integer'),
        (STRING, 'String'),
    )

    # Term type choices
    CONSTANT = 0
    DEFINITION = 1
    INPUT = 2
    OUTPUT = 3
    VARIABLE = 4

    T_TYPE_CHOICES = (
        (CONSTANT, 'Constant'),
        (DEFINITION, 'Definition'),
        (INPUT, 'Input'),
        (OUTPUT, 'Output'),
        (VARIABLE, 'Variable'),
    )

    d_type = models.IntegerField('Data Type', choices=D_TYPE_CHOICES, default=NONE)
    name = models.CharField(max_length=140, unique=True)
    t_type = models.IntegerField('Term Type', choices=T_TYPE_CHOICES,
                                 default=DEFINITION)
    boolean_false_cond = models.CharField('Boolean True Condition', max_length=140, blank=True,
                                          null=True)
    boolean_true_cond = models.CharField('Boolean False Condition', max_length=140, blank=True,
                                         null=True)
    enumerators = models.JsonField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    max_value = models.CharField('Maximum Value', max_length=140, blank=True, null=True)
    min_value = models.CharField('Minimum Value', max_length=140, blank=True, null=True)
    units = models.ForeignKey(Unit, blank=True, null=True, on_delete=models.CASCADE)
    initial_value = models.CharField(max_length=140, blank=True, null=True)
    value = models.CharField(max_length=140, blank=True, null=True)

    class Meta:
        app_label = 'requirements'
        ordering = ['name']

    def save(self, *args, **kwargs): # pylint: disable=signature-differs
        '''
        Override superclass save to:
         * make `boolean_false_cond` field string upper if filled
         * make `boolean_true_cond` field string upper if filled
        '''

        if self.boolean_false_cond:
            self.boolean_false_cond = self.boolean_false_cond.upper()

        if self.boolean_true_cond:
            self.boolean_true_cond = self.boolean_true_cond.upper()

        # Call superclass save
        super().save(*args, **kwargs)

    def __str__(self):
        return '"{}"'.format(self.name)


@reversion.register()
class SysReq(CoreModel):
    '''
    Defines database table structure for `SysReq` entries

    System requirements are the input to the project and define system level
    functionality
    '''

    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    req_statement = models.TextField('Requirement Statement')

    class Meta:
        app_label = 'requirements'
        verbose_name = 'System Requirement'
        verbose_name_plural = 'System Requirements'


@reversion.register()
class HighLevelReq(CoreModel):
    '''
    Defines database table structure for `HighLevelReq` entries

    High level requirements define high level functionality translated from system
    requirements
    '''

    derived_req = models.BooleanField(default=False)
    req_statement = models.TextField('Requirement Statement')
    sys_req = models.ManyToManyField(SysReq, verbose_name='System Requirement')
    term = models.ManyToManyField(Term, verbose_name='Terms')

    class Meta:
        app_label = 'requirements'
        verbose_name = 'High-level Requirement'
        verbose_name_plural = 'High-level Requirements'


@reversion.register()
class LowLevelReq(CoreModel):
    '''
    Defines database table structure for `LowLevelReq` entries

    Low level requirements define low level functionality translated from high-level
    requirements
    '''

    derived_req = models.BooleanField(default=False)
    high_level_req = models.ManyToManyField(
        HighLevelReq, verbose_name='High-level Requirement'
    )
    req_statement = models.TextField('Requirement Statement')
    term = models.ManyToManyField(Term, verbose_name='Terms')

    class Meta:
        app_label = 'requirements'
        verbose_name = 'Low-level Requirement'
        verbose_name_plural = 'Low-level Requirements'
