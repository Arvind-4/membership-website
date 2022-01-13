from logging import RootLogger
import uuid
from datetime import datetime
from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine import columns
from django.conf import settings
from django.http import Http404

from videos.models import Video
from videos.extractor import extract_video_id

# Create your models here.

class Playlist(DjangoCassandraModel):
    __keyspace__ = settings.KEYSPACE
    db_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    user_id = columns.UUID()
    updated = columns.DateTime(default=datetime.utcnow())
    host_ids = columns.List(value_type=columns.Text, default=[])
    title = columns.Text()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'{self.title}| {self.host_ids}'

    def get_videos(self):
        videos = []
        for host_id in self.host_ids:
            try:
                video_obj = Video.objects.filter(host_id=host_id).first()
            except:
                video_obj = None
            if video_obj is not None:
                videos.append(video_obj)
        return videos

    @staticmethod
    def get_host_id_from_url(url, flag=False):
        found = extract_video_id(url=url)
        if not found:
            flag = False
        else:
            flag = True
        return (flag, found)
    
    @staticmethod
    def exists_or_not(obj, url_extracted, exists_flag=False):
        if len(list(obj.host_ids)) > 1:
            for host_id in list(obj.host_ids):
                if host_id in url_extracted:
                    exists_flag = True
        return exists_flag

    @staticmethod
    def add_video_to_playlist(obj=None, value=None, exists=False, replace_all=False, saved=False):
        if exists:
            saved = False
        else:
            if replace_all:
                obj.host_ids = value
            else:
                obj.host_ids += value
            saved = True
        obj.save()
        return saved, obj

    @staticmethod
    def get_or_create_playlist(host_ids=[], user_id=None, title=None, replace_all=False):
        if not isinstance(host_ids, list):
            return False
        obj = Playlist(user_id=user_id, title=title)
        video_q = Video.objects.filter(host_id__in=host_ids)
        if not video_q.exists():
            return False
        if replace_all:
            obj.host_ids = host_ids
        else:
            if len(obj.host_ids) > 0:
                obj.host_ids += host_ids
                obj.updated = datetime.now()
                obj.save()
            else:
                obj = Playlist.objects.create(
                    host_ids=host_ids,
                    title=title,
                    user_id=user_id
                )
        return obj