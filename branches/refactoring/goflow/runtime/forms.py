#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from models import DefaultAppModel

from django.forms import ModelForm
from django import forms
from datetime import datetime


class BaseForm(ModelForm):
    '''
    base class for edition forms
    '''
    workitem_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    
    def save(self, workitem=None, submit_value=None, commit=True):
        obj = super(BaseForm, self).save(commit=commit)
        return obj
    
    def pre_check(self, obj_context=None, user=None):
        """may be overriden to do some check before.
        
        :param obj_context: object instance (if cmp_attr is set, this is the root object)
                            an exception should be risen if pre-conditions are not fullfilled
        """
        pass

    class Meta:
         exclude = ('workitem_id',)

class StartForm(ModelForm):
    '''
    base class for starting a workflow
    '''
    
    def save(self, user=None, data=None, commit=True):
        obj = super(StartForm, self).save(commit=commit)
        return obj
    
    def pre_check(self, user=None):
        """may be overriden to do some check before.
        
        an exception should be risen if pre-conditions are not fullfilled
        """
        pass


class DefaultAppForm(BaseForm):
    def save(self, workitem=None, submit_value=None, commit=True):
        obj = super(DefaultAppForm, self).save(commit=False)
        if obj.comment:
            if not obj.history:
                obj.history = 'Init'
            obj.history += '\n---------'
            if workitem:
                obj.history += '\nActivity: [%s]' % workitem.activity.title
            obj.history += '\n%s\n%s' % (datetime.now().isoformat(' '), obj.comment)
            obj.comment = None
        if submit_value:
            if obj.history:
                obj.history += '\n button clicked: [%s]' % submit_value
        obj.save()
        return obj

    class Meta:
         model = DefaultAppModel
         exclude = ('reason_denial',)


class DefaultAppStartForm(StartForm):
    def save(self,  user=None, data=None, commit=True):
        obj = super(DefaultAppStartForm, self).save(commit=False)
        if not obj.history:
            obj.history = 'Init'
        obj.history += '\n%s start instance' % datetime.now().isoformat(' ')
        if obj.comment:
            obj.history += '\n---------'
            obj.history += '\n%s' % obj.comment
            obj.comment = None
        obj.save()
        return obj

    class Meta:
         model = DefaultAppModel
         exclude = ('reason_denial',)

