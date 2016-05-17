# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def merge_muscles(apps, schema_editor):
    '''
    Merges the soleus muscle (ID 15) into gastrocnemius (ID 7) as the soleus
    is too small and specific. The gastrocnemius (calves) is enough for the
    "resolution" we need in this app.
    :return:
    '''
    Muscle = apps.get_model("exercises", "Muscle")

    # If there is no soleus, the database was newly created from the fixtures
    # which don't have it. In this case, there is nothing to do.
    try:
        soleus = Muscle.objects.get(pk=15)
    except Muscle.DoesNotExist:
        return

    gastrocnemius = Muscle.objects.get(pk=7)
    for exercise in soleus.exercise_set.all():
        # Add the gastrocnemius if its not already present, deleting the soleus
        # at the end of the migration will automatically remove it from the many
        # to many tables.

        # Main muscles
        if gastrocnemius not in exercise.muscles.all():
            exercise.muscles.add(gastrocnemius)

        # Secondary muscles
        if gastrocnemius not in exercise.muscles_secondary.all():
            exercise.muscles_secondary.add(gastrocnemius)

        exercise.save()
    soleus.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0002_auto_20150307_1841'),
    ]

    operations = [
        migrations.RunPython(merge_muscles)
    ]
