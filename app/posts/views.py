from comments.forms import CommentForm
from comments.models import Comment

from utils.auth import auth_check
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import PostFrom
from .models import Post


@auth_check
def posts_create(request):
    print timezone.now().time()
    form = PostFrom(request.POST or None, request.FILES or None, initial={"publish": timezone.now()}) # request.POST or None - for post date we need to validate it

    if form.is_valid():
        instance = form.save(commit=False)
        # for check send data we need to use:
        # form.cleaned_data.get('title')
        instance.user = request.user
        instance.save()
        messages.success(request, 'Successfully created!', extra_tags='message-box') # extra_tags - add class
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, 'Not created!')

    context = {
        'form': form
    }
    return render(request, 'post_form.html', context)

def posts_list(request):
    today = timezone.now().date()
    isSuperuser = request.user.is_superuser
    # hide draft and hide posts what will be create in a future time
    queryset_list = Post.objects.active()
    # if we superuser or staff we get full list
    if request.user.is_staff or isSuperuser:
        queryset_list = Post.objects.all()

    # if we send query for search
    query = request.GET.get('query')
    if query:
        queryset_list = queryset_list.filter(
            # if we want to search about title AND content AND user
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    paginator = Paginator(queryset_list, 5)  # Show 25 contacts per page
    page_request_var = 'page'
    page = request.GET.get(page_request_var) # page - is query in browser url. For example: /posts/?page=1
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        'object_list': queryset,
        'title': 'List',
        'page_request_var': page_request_var,
        'today': today,
        'isSuperuser': isSuperuser
    }
    return render(request, 'post_list.html', context)

@auth_check
def posts_update(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    form = PostFrom(request.POST or None, request.FILES or None, instance=instance)  # request.POST or None - for post date we need to validate it, instance - this is post

    if form.is_valid():
        instance = form.save(commit=False)
        # for check send data we need to use:
        # form.cleaned_data.get('title')
        instance.save()
        # extra_tags - add class
        # if we use tags in message, we need to put to the template statement when - if we set html_safe class we render in safe mode
        messages.success(request, '<a href=/posts/' + str(instance.id) + '>Item</a> Updated!', extra_tags='message-box html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'title': 'Detail',
        'instance': instance,
        'form': form
    }
    return render(request, 'post_form.html', context)

def posts_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    # if post is draft we need to hide it for unauth user
    print instance.publish
    print timezone.now()
    if instance.draft or instance.publish > timezone.now():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    initial_data = {
        'content_type': instance.get_content_type,
        'object_id': instance.id
    }

    comment_form = CommentForm(request.POST or None, initial=initial_data)

    if comment_form.is_valid() and request.user.is_authenticated():
        c_type = comment_form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        obj_id = comment_form.cleaned_data.get('object_id')
        content_data = comment_form.cleaned_data.get('content')
        # Replies for comment
        parent_obj = None
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comments = instance.comments

    context = {
        'title': 'Detail',
        'instance': instance,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'post_detail.html', context)

@auth_check
def posts_delete(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, 'Successfully deleted!', extra_tags='message-box')  # extra_tags - add class
    return redirect('posts:list')