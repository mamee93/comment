from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.dispatch import receiver
from django.urls import reverse
from django.contrib import messages




 
# Create your views here.

class Post(models.Model):
	 

	STATUS_CHOICES = (
		('draft','Draft'),
		('publshed','Publshed'),

		)
 
	title   = models.CharField(max_length=220)
	content = models.TextField(max_length=1000, blank=True)
	slug    = models.SlugField(max_length=120)
	author  = models.ForeignKey(User,related_name='blog_post', on_delete=models.CASCADE)
	likes   = models.ManyToManyField(User, related_name='likes',blank=True )
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status  = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:detail_post', args=[self.slug])

	def total_like(self):
		return self.likes.count()

	# def save(self, *args, **kwargs):
 #        self.slug = self.title
 #        super(Post,self).save(*args, **kwargs)


@receiver(pre_save, sender=Post)
def pre_save_slug(sender, **kwargs):
	slug = slugify(kwargs['instance'].title)
	kwargs['instance'].slug = slug

# class Images(models.Model):
# 	post = models.ForeignKey(Post,on_delete=models.CASCADE)
# 	image = models.ImageField(upload_to='images/', blank=True,null=True)

# 	def __str__(self):
# 		return self.post

class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=250)
    reply = models.ForeignKey('self', related_name='replies' ,on_delete=models.CASCADE,null=True)
    created = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return '{}-{}'.format(self.post.title, str(self.user.username))
    
	 
	