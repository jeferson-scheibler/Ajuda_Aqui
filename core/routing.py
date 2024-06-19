from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/edit_task/(?P<task_id>\d+)/$', consumers.TaskEditConsumer.as_asgi()),
]