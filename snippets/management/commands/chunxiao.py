# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument("name", type=str)
		parser.add_argument("id", type=int)

	def handle(self, *args, **options):
		id = options["id"]
		name = options["name"]
		user = User.objects.all().first()
		print id, name, user.username
