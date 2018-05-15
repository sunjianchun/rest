# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from models import *
# Create your tests here.

class SnippetTestCase(TestCase):
	def setUp(self):
		print "StartUp test..."
		self.snippet = Snippet(title='test', code='hello, world')
	def test_snippet_style(self):
		self.assertEqual(self.snippet.style, "friendly")
