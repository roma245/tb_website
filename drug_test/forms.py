from django import forms
from .models import Post

class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('title', 'text',)



class SrrForm(forms.ModelForm):

	class Meta:
		model = PostSRR
		fields = ('srr_id',)
