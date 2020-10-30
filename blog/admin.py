from django.contrib import admin
from .models import Post,Comment,Vote
# Register your models here.

class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'author' , 'status')
	list_filterv= ('status', 'created', 'updated')
	search_fields = ('author__username', 'title')
	prepopulated_fields = {'slug':('title',)}
	list_editable = ('status',)
	date_hierarchy = ('created')

admin.site.register(Post,PostAdmin)
admin.site.register(Comment)
admin.site.register(Vote)