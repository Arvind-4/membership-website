from django.urls import path

from .views import (
    playlist_create_view,
    playlist_list_view,
    playlist_detail_view,
    playlist_delete_view,
    playlist_edit_view,

    playlist_delete_video,
    playlist_add_videos,
)

urlpatterns = [
    path('create-view/', playlist_create_view, name='playlist-create'),
    path('list-view/', playlist_list_view, name='playlist-list'),
    path('<str:user_id>/edit-view/<str:db_id>/', playlist_edit_view, name='playlist-edit'),
    path('<str:user_id>/detail-view/<str:db_id>/', playlist_detail_view, name='playlist-detail'),
    path('<str:user_id>/delete-video/<str:db_id>/', playlist_delete_view, name='playlist-delete'),

    path('<str:user_id>/add-video/<str:db_id>/', playlist_add_videos, name='playlist-add'),
    path('<str:user_id>/remove-video/<str:db_id>/<str:host_id>/', playlist_delete_video, name='playlist-remove'),
]