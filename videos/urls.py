from django.urls import path

from .views import (
    video_list_view,
    video_detail_view,
    video_create_view,
    video_edit_view,
    video_delete_view
)

urlpatterns = [
    path('create-view/', video_create_view, name='video-create'),
    path('list-view/', video_list_view, name='video-list'),
    path('detail-view/<str:host_id>/<str:db_id>/', video_detail_view, name='video-detail'),
    path('edit-view/<str:host_id>/<str:db_id>/', video_edit_view, name='video-edit'),
    path('delete-view/<str:host_id>/<str:db_id>/', video_delete_view, name='video-delete'),
]