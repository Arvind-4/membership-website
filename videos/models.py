import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel
from django.conf import settings

from .extractor import extract_video_id

class Video(DjangoCassandraModel):
    __keyspace__ = settings.KEYSPACE
    host_id = columns.Text(primary_key=True)
    db_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    host_service = columns.Text(default='youtube')
    title = columns.Text()
    url = columns.Text()
    user_id = columns.UUID()

    class Meta:
        get_pk_field = 'db_id'

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.title} | {self.host_id}"


    @staticmethod
    def add_or_get_video(title, url, user_id=None, edit_data=False, *args, **kwargs):
        created = False
        obj = None
        saved = False
        host_id = extract_video_id(url)
        if host_id is None:
            raise ValueError("Invalid YouTube Video URL")
        if not edit_data:  
            qs_find = Video.objects.filter(host_id=host_id, user_id=user_id)
            if qs_find.exists():
                obj = qs_find.first()
                created = False
            else:
                obj = Video.objects.create(
                    title=title,
                    host_id=host_id,
                    user_id=user_id,
                    url=url
                )
                created = True
                saved = True
        else:
            obj = Video.objects.get(host_id=host_id, user_id=user_id)
            obj.url = url
            obj.title = title
            obj.host_id = host_id
            obj.user_id = user_id
            obj.save()
        return obj, created, saved