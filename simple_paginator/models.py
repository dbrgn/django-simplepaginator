from django.db import models
from django import test

class MockModel(models.Model):
	char_field = models.CharField(max_length=10)
	integer_field = models.IntegerField()
	second_integer_field = models.IntegerField()

	def testmethod(self):
		return self.integer_field + self.second_integer_field