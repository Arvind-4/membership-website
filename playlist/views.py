from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from videos.models import Video

from .forms import (
    PlayListCreateForm,
)
from .models import Playlist

# Create your views here.

@login_required
def playlist_create_view(request, *args, **kwargs):
    form = PlayListCreateForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        title = form.cleaned_data.get('title')
        obj = Playlist.objects.create(
            user_id=request.user.id,
            title=title
        )
        if request.htmx:
            context['object'] = obj
            return render(request, 'playlist/snippits/list-inline.html', context)
        # return redirect('playlist-list')
    return render(request, 'playlist/create-view.html', context=context)

@login_required
def playlist_edit_view(request, db_id, user_id):
    qs = Playlist.objects.filter(db_id=db_id, user_id=user_id)
    if not qs.exists():
        raise Http404
    initial_data = {
        'title': qs.first().title
    }
    obj_old = qs.first()
    form = PlayListCreateForm(request.POST or None, initial=initial_data)
    context = {
        'form': form,
        'object': obj_old
    }
    if form.is_valid():
        new_title = form.cleaned_data.get('title')
        obj = qs.first()
        obj.title = new_title
        obj.save()
        if request.htmx:
            context['message'] = True
            context['object'] = obj
            return render(request, 'playlist/snippits/list-inline.html', context)
    return render(request, 'playlist/edit-view.html', context)

@login_required
def playlist_list_view(request, *args, **kwargs):
    qs = Playlist.objects.filter(user_id=request.user.id)
    if qs.exists():
        obj = qs
    else:
        obj = []
    context = {
        'object_list': list(obj) or []
    }
    return render(request, 'playlist/list-view.html', context=context)

@login_required
def playlist_detail_view(request, user_id, db_id, *args, **kwargs):
    obj = Playlist.objects.filter(user_id=user_id, db_id=db_id)
    if not obj.exists():
        raise Http404
    context = {
        'object': obj.first(),
        'video_object_list': obj.first().get_videos()
    }
    return render(request, 'playlist/detail-view.html', context)


@login_required
def playlist_delete_view(request, user_id, db_id, *args, **kwargs):
    qs = Playlist.objects.filter(db_id=db_id, user_id=user_id)
    deleted = False
    if qs.exists():
        qs.first().delete()
        deleted = True
    if deleted:
        return HttpResponse('')
    else:
        raise Http404















































@login_required
def playlist_add_videos(request, user_id, db_id, *args, **kwargs):
    obj = Playlist.objects.filter(user_id=user_id, db_id=db_id)
    if not obj.exists():
        raise Http404
    context = {
        'object': obj.first(),
        'object_list': list(Video.objects.filter(user_id=request.user.id))
    }
    if request.method == 'POST':
        video_list = request.POST.getlist('playlist_videos')
        # exists_flag = obj.first().exists_or_not(obj=obj.first(), url_extracted=video_list)
        saved, qs_object = obj.first().add_video_to_playlist(obj=obj.first(), value=video_list)
        if request.htmx:
            context['video_object_list'] = qs_object.get_videos()
            return render(request, 'playlist/snippits/detail-inline.html', context=context)
    return render(request, 'playlist/add-video.html', context=context)


@login_required
def playlist_delete_video(request, user_id, db_id, host_id, *args, **kwargs):
    obj = Playlist.objects.filter(user_id=user_id, db_id=db_id)
    if not obj.exists():
        raise Http404
    obj.first().host_ids.remove(host_id)
    obj.first().save()
    return HttpResponse('')