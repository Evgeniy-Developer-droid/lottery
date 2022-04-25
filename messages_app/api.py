from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse
from messages_app.models import RoomUser, Message, Room
from django.templatetags.static import static


def get_contacts(request):
    response = list()
    rooms = [item.room.pk for item in RoomUser.objects.filter(user=request.user.pk)]
    companions = RoomUser.objects.filter(room__in=rooms).exclude(user=request.user.pk)[::-1]
    for companion in companions:
        response.append({
            "user_id": companion.user.pk,
            "room_id": companion.room.pk,
            "name": companion.user.first_name + " " + companion.user.last_name,
            "icon": companion.user.profile.image.url if companion.user.profile.image else static('public/img/default-user-icon.jpg'),
            "new": Message.objects.filter(receiver=request.user.pk, sender=companion.user.pk, read=False).count()
        })
    return JsonResponse(response, safe=False)


def get_messages(request):
    response = {'messages':[]}
    companion = RoomUser.objects.filter(room=request.POST.get('room')).exclude(user=request.user.pk)
    if companion.exists():
        companion = companion.first()
        response['companion'] = dict()
        response['companion']['name'] = companion.user.first_name + " " + companion.user.last_name
        response['companion']['user_id'] = companion.user.pk
        response['companion']['icon'] = companion.user.profile.image.url if companion.user.profile.image else static('public/img/default-user-icon.jpg')
    messages = Message.objects.filter(room=request.POST.get('room'))
    for message in messages:
        response['messages'].append({
            "timestamp": message.timestamp,
            "name": message.sender.first_name + " " + message.sender.last_name,
            "user_id": message.sender.pk,
            "icon": message.sender.profile.image.url if message.sender.profile.image else static('public/img/default-user-icon.jpg'),
            "body": message.body
        })
    return JsonResponse(response)


def post_message(request):
    body = request.POST.get('body', "")
    receiver = User.objects.get(pk=request.POST.get('receiver', ""))
    room = Room.objects.get(pk=request.POST.get('room', ""))
    if body:
        mess = Message(sender=request.user, receiver=receiver, body=body, room=room)
        mess.save()
        data = {
            "timestamp": mess.timestamp,
            "name": mess.sender.first_name + " " + mess.sender.last_name,
            "user_id": mess.sender.pk,
            "icon": mess.sender.profile.image.url if mess.sender.profile.image else static('public/img/default-user-icon.jpg'),
            "body": mess.body
        }
        layer = get_channel_layer()
        async_to_sync(layer.group_send)('events_'+str(receiver.pk), {
            'type': 'events.alarm',
            'content': {
                'type': "message",
                'room': room.pk,
                "name": mess.sender.first_name + " " + mess.sender.last_name,
                "user_id": mess.sender.pk,
                "icon": mess.sender.profile.image.url if mess.sender.profile.image else static('public/img/default-user-icon.jpg'),
                "body": mess.body
            }
        })
        return JsonResponse({'message':'OK', "type":"success", "data": data})
    return JsonResponse({'message': 'Failed', "type": "error"})


def read_messages(request):
    room = int(request.POST.get('room', 0))
    messages = Message.objects.filter(receiver=request.user.pk, room=room, read=False)
    if messages.exists():
        messages.update(read=True)
    return JsonResponse({'message': "OK", 'type': "success"})


def check_exist_room(now_user, target_user):
    rooms_now_user = [item.room.pk for item in RoomUser.objects.filter(user=now_user.pk)]
    rooms_target_user = [item.room.pk for item in RoomUser.objects.filter(user=target_user.pk)]
    for elem in rooms_now_user:
        if elem in rooms_target_user:
            return elem
    return False


def create_dialog(request):
    response = dict()
    receiver = User.objects.get(pk=request.POST.get('receiver', ""))
    if receiver.pk == request.user.pk:
        response['message'] = "You cannot create dialog!"
        response['type'] = "error"
        return JsonResponse(response)
    room_exist = check_exist_room(request.user, receiver)
    if room_exist:
        return JsonResponse({"url": reverse("messages") + "?dialog=" + str(room_exist)})
    room = Room()
    room.save()
    RoomUser(user=receiver, room=room).save()
    RoomUser(user=request.user, room=room).save()
    return JsonResponse({"url": reverse("messages") + "?dialog=" + str(room.pk)})

