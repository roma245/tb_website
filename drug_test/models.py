from django.db import models
from django.utils import timezone


def invoke_galaxy_wf(srr_input):
	return '33b43b4e7093c91f'




class Post(models.Model):
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title



class PostSRR(models.Model):

	author = models.ForeignKey('auth.User')
	srr_input = models.CharField(max_length=10)
	created_date = models.DateTimeField(default=timezone.now)

	invoked_wf = invoke_galaxy_wf(srr_input)
	dataset_link = ''


	def __str__(self):
		return self.title






