from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .forms import AddVideoForm
from .models import Video

# Create your views here.

@login_required
def video_create_view(request):
    form = AddVideoForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        cleaned_url = form.cleaned_data.get('url')
        cleaned_title = form.cleaned_data.get('title')
        obj, created, saved = Video.add_or_get_video(
            title=cleaned_title,
            url=cleaned_url,
            user_id=request.user.id
        )
        if saved:
            return redirect('video-list')
    return render(request, 'videos/create-view.html', context)

@login_required
def video_list_view(request):
    form = AddVideoForm(request.POST or None)
    context = {
        'form': form,
        'object_list': list(Video.objects.filter(user_id=request.user.id)) or []
    }
    return render(request, 'videos/list-view.html', context)

@login_required
def video_detail_view(request, db_id, host_id):
    obj = Video.objects.filter(host_id=host_id, db_id=db_id)
    if not obj.exists():
        raise Http404
    context = {
        'object': obj.first()
    }
    return render(request, 'videos/detail-view.html', context)

@login_required
def video_edit_view(request, db_id, host_id):
    qs = Video.objects.filter(host_id=host_id, db_id=db_id, user_id=request.user.id)
    if not qs.exists():
        raise Http404
    initial_data = {
        'url': qs.first().url,
        'title': qs.first().title
    }
    obj_old = qs.first()
    form = AddVideoForm(request.POST or None, initial=initial_data)
    context = {
        'form': form,
        'object': obj_old
    }
    if form.is_valid():
        new_url = form.cleaned_data.get('url')
        new_title = form.cleaned_data.get('title')
        obj, created, saved = Video.add_or_get_video(
            title=new_title,
            url=new_url,
            user_id=request.user.id,
            edit_data=True
        )
        if request.htmx:
            context['message'] = True
            context['object'] = obj
            return render(request, 'videos/snippits/list-inline.html', context)
    return render(request, 'videos/edit-view.html', context)

@login_required
def video_delete_view(request, db_id, host_id):
    qs = Video.objects.allow_filtering().filter(host_id=host_id, db_id=db_id)
    if qs.count() == 1:
        qs.delete()
        return HttpResponse('')
    else:
        raise Http404