from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core import serializers

from .models import Forum, ForumReply
from .forms import ForumForm, ForumReplyForm

# Create your views here.


@login_required(login_url=reverse_lazy('auths:login'))
def create_forum(request):
    # check if user role is READER
    if request.user.role != 'READER' and request.user.role != 'AUTHOR':
        return HttpResponseForbidden('FORBIDDEN')

    # create forum form
    form = ForumForm(request.POST or None)

    # if user upload form, then save form
    if form.is_valid() and request.method == 'POST':
        forum = form.save(commit=False)
        forum.forum_creator_id = request.user
        forum.save()

        return HttpResponseRedirect(reverse('forum:display_all_forum'))

    context = {'form': form, 'role': request.user.role}
    return render(request, "create_forum.html", context)


@login_required(login_url=reverse_lazy('auths:login'))
def display_all_forum(request):
    # return forbidden if user role is not READER
    if request.user.role != 'READER' and request.user.role != 'AUTHOR':
        return HttpResponseForbidden('FORBIDDEN')

    # get all forums from db
    forums = Forum.objects.all()
    print(forums)

    context = {'forums': forums, 'role': request.user.role}
    return render(request, 'all_forums.html', context)


@login_required(login_url=reverse_lazy('auths:login'))
def display_forum_by_id(request, forum_id):
    if request.user.role != 'READER' and request.user.role != 'AUTHOR':
        return HttpResponseForbidden('FORBIDDEN')

    forum = Forum.objects.get(pk=forum_id)
    replies = ForumReply.objects.filter(forum_id=forum_id)

    reply_form = ForumReplyForm(request.POST or None)

    if reply_form.is_valid() and request.method == 'POST':
        reply = reply_form.save(commit=False)
        reply.commentor_id = request.user
        reply.forum_id = forum
        forum.num_comments += 1
        forum.save()
        reply.save()
        # replies = ForumReply.objects.filter(forum_id=forum_id)

    context = {'forum': forum, 'replies': replies,
               'reply_form': reply_form, 'role': request.user.role}
    return render(request, 'forum_details.html', context)


@login_required(login_url=reverse_lazy('auths:login'))
def display_all_forums_ajax(request):
    print(request.user.role)
    if request.user.role != 'READER' and request.user.role != 'AUTHOR':
        return HttpResponseForbidden('FORBIDDEN')

    forums = Forum.objects.all()
    json_response = []

    for forum in forums:
        print(forum)

        forum_json = {
            'forumDetailLink': f'/forum/{forum.forum_id}',
            'forumTitle': forum.forum_title,
            'book': {
                'cover': forum.book_topic.book_cover_link,
                'title': forum.book_topic.book_title
            },
            'creatorUsername': forum.forum_creator_id.username,
            'numberOfComments': forum.num_comments
        }

        json_response.append(forum_json)

    return JsonResponse({'forums': json_response})

    # forums = Forum.objects.all()

    # return HttpResponse(serializers.serialize("json", forums), content_type="application/json")
