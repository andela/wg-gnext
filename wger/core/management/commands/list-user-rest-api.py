# -*- coding: utf-8 *-*

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

import sys

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from wger.core.models import RestUser


class Command(BaseCommand):
    '''
    Handle command to list users created via REST API
    '''
    help = 'List users created via REST API'

    def add_arguments(self, parser):
        '''
        define arguments required
        '''
        parser.add_argument(
            '-a',
            '--all',
            action='store_true',
            dest='all',
            help='List all users created via REST API',
            default=True)

        parser.add_argument(
            '-u',
            '--username',
            action='store',
            dest='username',
            help='List all users created via REST API by a given user',
            default=None
        )

    def handle(self, *args, **options):
        '''
        main method to execute command
        '''
        username = options['username']
        if not username:  # if username is not provided, list all users.
            rest_users = (user for user in RestUser.objects.all())
            for user in rest_users:
                date = user.timestamp.strftime("%Y-%m-%d")
                self.stdout.write(
                    self.style.SUCCESS(
                        'USER:"%s" DATE-ADDED: %s' % (user, date)))
            sys.exit(0)

        try:
            # list users created by the provided user
            user = User.objects.get(username=username)

            # list users
            rest_users = (user for user in RestUser.objects.filter(created_by=user))
            for user in rest_users:
                date = user.timestamp.strftime("%Y-%m-%d")
                self.stdout.write(
                    self.style.SUCCESS(
                        'USER:"%s" DATE-ADDED: %s' % (user, date)))

        except User.DoesNotExist:
            # raise error if user does not exist
            raise CommandError('user with "%s" username does not exist' % username)
