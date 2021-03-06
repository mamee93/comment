from django.shortcuts import render,get_object_or_404,redirect,Http404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Post,Comment,Vote
from django.http import HttpResponseRedirect, JsonResponse
from .forms import  PostCreateForm,CommentForm
from  django.template.loader import render_to_string
from django.db.models import F
from django.db.models import Q
# from django.urls import reverse

# Create your views here.

def all_list(request):
	all_list = Post.objects.all()
	return render(request,'post/post_list.html',{'all_list':all_list}) 

@login_required
def post_create(request):

	if request.method == "POST":
		form = PostCreateForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('blog:all_list')
	else:
		form = PostCreateForm()
	return render(request, 'post/post_create.html',{'form':form})

 

def detail(request,slug):
	post = get_object_or_404(Post,slug=slug)
	comments = Comment.objects.filter(post=post,reply=None).order_by('-id')
	is_liked = False
	if post.likes.filter(id=request.user.id).exists():
		is_liked = True

	if request.method == "POST":
		comment_form = CommentForm(request.POST or None)
		if comment_form.is_valid():
			content  = request.POST.get('content')
			reply_id = request.POST.get('comment_id')
			comment_qs = None
			if reply_id:
				comment_qs = Comment.objects.get(id=reply_id)
			comment  = Comment.objects.create(post=post, user=request.user, content=content,reply=comment_qs)
			comment.save()
			#return HttpResponseRedirect(post.get_absolute_url())
	else:
		comment_form = CommentForm()
	context = {'post':post,'is_liked':is_liked,
		'total_like':post.total_like(),'comments':comments,'comment_form':comment_form}

	if request.is_ajax():
		html = render_to_string('post/comment.html',context,request=request)
		return JsonResponse({'form':html})
		
	return render(request, 'post/detail.html',context)

@login_required
def post_edit(request,slug):
    post = get_object_or_404(Post,slug=slug)
    if post.author != request.user:
    	raise Http404()
    if request.method == 'POST':   
        form = PostCreateForm(request.POST, request.FILES ,instance = post)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.author = request.user
            myform.save()
            return HttpResponseRedirect(post.get_absolute_url())
            #return redirect('/')
    else:
        form = PostCreateForm(instance = post)

    return render(request,'post/edit_post.html',{'form':form,'posts':post})


def post_delete(request, slug):
	post = get_object_or_404(Post,slug=slug)
	if request.user != post.author:
		raise Http404()
	post.delete()
	return redirect('blog:all_list')


def like_post(request):

	#post = get_object_or_404(Post,id=request.POST.get('post_id'))
	post = get_object_or_404(Post,id=request.POST.get('id'))
	is_liked = False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		is_liked = False
	else:
		post.likes.add(request.user)
		is_liked = True 
	context ={
		'post':post,
		'is_liked':is_liked,
		'total_like':post.total_like()
	}
	if request.is_ajax():
		html = render_to_string('post/like_section.html',context,request=request)
		return JsonResponse({'form':html})
	# return  HttpResponseRedirect(post.get_absolute_url())


def thumbs(request):

    if request.POST.get('action') == 'thumbs':

        id = int(request.POST.get('postid'))
        button = request.POST.get('button')
        update = Post.objects.get(id=id)

        if update.thumbs.filter(id=request.user.id).exists():

            # Get the users current vote (True/False)
            q = Vote.objects.get(
                Q(post_id=id) & Q(user_id=request.user.id))
            evote = q.vote

            if evote == True:

                # Now we need action based upon what button pressed

                if button == 'thumbsup':

                    update.thumbsup = F('thumbsup') - 1
                    update.thumbs.remove(request.user)
                    update.save()
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown
                    q.delete()

                    return JsonResponse({'up': up, 'down': down, 'remove': 'none'})

                if button == 'thumbsdown':

                    # Change vote in Post
                    update.thumbsup = F('thumbsup') - 1
                    update.thumbsdown = F('thumbsdown') + 1
                    update.save()

                    # Update Vote

                    q.vote = False
                    q.save(update_fields=['vote'])

                    # Return updated votes
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown

                    return JsonResponse({'up': up, 'down': down})

            pass

            if evote == False:

                if button == 'thumbsup':

                    # Change vote in Post
                    update.thumbsup = F('thumbsup') + 1
                    update.thumbsdown = F('thumbsdown') - 1
                    update.save()

                    # Update Vote

                    q.vote = True
                    q.save(update_fields=['vote'])

                    # Return updated votes
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown

                    return JsonResponse({'up': up, 'down': down})

                if button == 'thumbsdown':

                    update.thumbsdown = F('thumbsdown') - 1
                    update.thumbs.remove(request.user)
                    update.save()
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown
                    q.delete()

                    return JsonResponse({'up': up, 'down': down, 'remove': 'none'})

        else:        # New selection

            if button == 'thumbsup':
                update.thumbsup = F('thumbsup') + 1
                update.thumbs.add(request.user)
                update.save()
                # Add new vote
                new = Vote(post_id=id, user_id=request.user.id, vote=True)
                new.save()
            else:
                # Add vote down
                update.thumbsdown = F('thumbsdown') + 1
                update.thumbs.add(request.user)
                update.save()
                # Add new vote
                new = Vote(post_id=id, user_id=request.user.id, vote=False)
                new.save()

            # Return updated votes
            update.refresh_from_db()
            up = update.thumbsup
            down = update.thumbsdown

            return JsonResponse({'up': up, 'down': down})

    pass







































