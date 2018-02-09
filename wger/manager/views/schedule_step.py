# -*- coding: utf-8 -*-

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

import logging

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy, ugettext as _
from django.db import models

from django import forms
from django.views.generic import (CreateView, DeleteView, UpdateView)

from wger.manager.models import (Schedule, ScheduleStep, Workout)
from wger.manager.helpers import (MACROCYCLE, MESOCYLCLE, MICROCYCLE, periodization)
from wger.utils.generic_views import (WgerFormMixin, WgerDeleteMixin)

logger = logging.getLogger(__name__)

PERIODIZATION_CHOICES = (
    (periodization.get_max(MICROCYCLE),
     '%s(1 week)' % MICROCYCLE.capitalize()),
    (periodization.get_max(MESOCYLCLE),
     '%s(2-6 weeks)' % MESOCYLCLE.capitalize()),
    (periodization.get_max(MACROCYCLE),
     '%s(1 year)' % MACROCYCLE.capitalize()),
)

class StepCreateView(WgerFormMixin, CreateView, PermissionRequiredMixin):
    '''
    Creates a new workout schedule
    '''

    model = ScheduleStep
    fields = '__all__'
    title = ugettext_lazy('Add workout')

    def get_form_class(self):
        '''
        The form can only show the workouts belonging to the user.

        This is defined here because only at this point during the request
        have we access to the current user
        '''

        class StepForm(forms.ModelForm):
            workout = forms.ModelChoiceField(
                queryset=Workout.objects.filter(user=self.request.user))

            class Meta:
                model = ScheduleStep
                exclude = ('order', 'schedule', 'is_periodized')

            def __init__(self, *args, **kwargs):
                if 'schedule_pk' in kwargs:
                    self.schedule_pk = kwargs.pop('schedule_pk')

                super(StepForm, self).__init__(*args, **kwargs)

                if hasattr(self, 'schedule_pk'):
                    schedule = Schedule.objects.get(pk=self.schedule_pk)

                    if getattr(schedule, 'use_periodization'):
                        del self.fields['duration']
                        new_duration_field = forms.ChoiceField(choices=PERIODIZATION_CHOICES)
                        self.fields['duration'] = new_duration_field

        return StepForm

    def get_form_kwargs(self):
        kwargs = super(StepCreateView, self).get_form_kwargs()

        if 'schedule_pk' not in kwargs:
            kwargs['schedule_pk'] = self.kwargs.get('schedule_pk')

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(StepCreateView, self).get_context_data(**kwargs)
        context['form_action'] = reverse(
            'manager:step:add',
            kwargs={
                'schedule_pk': self.kwargs['schedule_pk']
            })
        return context

    def get_success_url(self):
        return reverse(
            'manager:schedule:view', kwargs={
                'pk': self.kwargs['schedule_pk']
            })

    def form_valid(self, form):
        '''Set the schedule and the order'''
        uses_periodization = False
        schedule = Schedule.objects.get(pk=self.kwargs['schedule_pk'])

        if schedule.use_periodization:
            # mark schedule step as periodized plan.
            form.instance.is_periodized = True
            uses_periodization = True

        if not uses_periodization and form.cleaned_data['duration'] > 25:
            # normal scheduled steps should not exceed 25 weeks
            form.add_error('duration', 'Ensure that duration value is equal or less than 25')
            return super(StepCreateView, self).form_invalid(form)

        max_order = schedule.schedulestep_set.all().aggregate(
            models.Max('order'))
        form.instance.schedule = schedule
        form.instance.order = (max_order['order__max'] or 0) + 1
        return super(StepCreateView, self).form_valid(form)


class StepEditView(WgerFormMixin, UpdateView, PermissionRequiredMixin):
    '''
    Generic view to update an existing schedule step
    '''

    model = ScheduleStep
    title = ugettext_lazy('Edit workout')
    form_action_urlname = 'manager:step:edit'

    def get_form_class(self):
        '''
        The form can only show the workouts belonging to the user.

        This is defined here because only at this point during the request
        have we access to the current user
        '''

        class StepForm(forms.ModelForm):
            workout = forms.ModelChoiceField(
                queryset=Workout.objects.filter(user=self.request.user))

            class Meta:
                model = ScheduleStep
                exclude = ('order', 'schedule')

        return StepForm


    def get_success_url(self):
        return reverse(
            'manager:schedule:view', kwargs={
                'pk': self.object.schedule_id
            })


class StepDeleteView(WgerDeleteMixin, DeleteView, PermissionRequiredMixin):
    '''
    Generic view to delete a schedule step
    '''

    model = ScheduleStep
    fields = ('workout', 'duration', 'order')
    form_action_urlname = 'manager:step:delete'
    messages = ugettext_lazy('Successfully deleted')

    def get_success_url(self):
        return reverse(
            'manager:schedule:view', kwargs={
                'pk': self.object.schedule.id
            })

    def get_context_data(self, **kwargs):
        '''
        Send some additional data to the template
        '''
        context = super(StepDeleteView, self).get_context_data(**kwargs)
        context['title'] = _(u'Delete {0}?').format(self.object)
        context['form_action'] = reverse(
            'core:license:delete', kwargs={
                'pk': self.kwargs['pk']
            })
        return context
