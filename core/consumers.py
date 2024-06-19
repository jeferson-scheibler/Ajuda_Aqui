import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Task

class TaskEditConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.task_group_name = f'task_{self.task_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.task_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.task_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        task_id = data['task_id']
        task_name = data['task_name']
        task_description = data['task_description']

        # Update task in database
        task = Task.objects.get(id=task_id)
        task.task_name = task_name
        task.task_description = task_description
        task.save()

        # Send task update to room group
        await self.channel_layer.group_send(
            self.task_group_name,
            {
                'type': 'task_update',
                'task_id': task_id,
                'task_name': task_name,
                'task_description': task_description
            }
        )

    async def task_update(self, event):
        task_id = event['task_id']
        task_name = event['task_name']
        task_description = event['task_description']

        # Send task update to WebSocket
        await self.send(text_data=json.dumps({
            'task_id': task_id,
            'task_name': task_name,
            'task_description': task_description
        }))