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
# along with Workout Manager.  If not, see <http://www.gnu.org/licenses/>.

"""
Nutrition app signal module.
"""


from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from wger.utils.cache import cache_mapper
from .models import NutritionPlan, Meal, MealItem


@receiver(post_save, sender=NutritionPlan)
@receiver(post_save, sender=Meal)
@receiver(post_save, sender=MealItem)
@receiver(post_delete, sender=NutritionPlan)
@receiver(post_delete, sender=Meal)
@receiver(post_delete, sender=MealItem)
def reset_cache(sender, instance, **kwargs):
    """
    We need to get nutritional plan id.

    Models that have relationship to NutritionalPlan model are:
        Meal -> plan
        MealItem -> meal -> plan

    Retrieving NutritionPlan instance is necessary so that we can
    be able to get object in cache and remove it.
    """
    pid = None

    if hasattr(instance, 'plan'):
        pid = getattr(instance, 'plan').pk


    elif hasattr(instance, 'meal'):
        pid = getattr(instance, 'meal').plan.pk

    else:
        pid = instance.pk

    # clear object in cache
    cache.delete(cache_mapper.get_nutritional_key(pid))
