from django import forms 
from  .models import Post,Comment

class PostCreateForm(forms.ModelForm):
	class Meta:
		model  = Post
		fields = ['title', 'content', 'status']

class CommentForm(forms.ModelForm):
	content = forms.CharField(label="",widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Comment here !!!', 'rows':'4','cols':'50'}))
	class Meta:
		model  = Comment
		fields = ['content',]