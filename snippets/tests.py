# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, SimpleTestCase
from models import *
from django.contrib.auth.models import User
from django.test import Client
#from django.test import Tag

class SnippetTestCaset(TestCase):
	fixtures = ['my_data.json']
	def setUp(self):
		print "StartUp test..." 
	#@Tag('fast')
	def test_snippet_style(self):
		response = self.client.login(username='sunjianchun', password='zaqzaqzaq')
		response = self.client.get('')

		self.assertEqual(response.status_code, 200)
	#@Tag('slow')
	def test_user_exists(self):
		response = self.client.login(username='sunjianchun', password='zaqzaqzaq')
		response = self.client.get('')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'http://')
