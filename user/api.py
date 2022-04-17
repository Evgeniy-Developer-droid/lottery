import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import JsonResponse
from user.Business.lottery_logic import (
    define_lottery_winners,
    permission_estimate,
    permission_complain
)
from user.models import Profile, Rating, Complain, Message, RoomUser


def define_winners(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if "id" not in data:
            return JsonResponse({'message': "Validation error! Set lottery id.", 'type': 'error'})
        response = define_lottery_winners(request, data)
        return JsonResponse(response, safe=False)
    return JsonResponse({'message': "Method GET not support", 'type': 'error'})


def change_user_avatar(request):
    if request.method == "POST":
        profile = Profile.objects.get(user=request.user.pk)
        profile.image = request.FILES.get("file")
        profile.save()
        return JsonResponse({'message': "Avatar updated!", 'type':'success'})
    return JsonResponse({'message': "Something wrong with file!", 'type':'warning'})


def change_user_data(request):
    response = dict()
    if request.POST.get('action') == "address":
        profile = Profile.objects.get(user=request.user.pk)
        profile.address = request.POST.get('value')
        profile.save()
        response['message'] = "Address has been updated"
        response['type'] = 'success'
    if request.POST.get('action') == "email":
        user = User.objects.get(pk=request.user.pk)
        user.email = request.POST.get('value')
        user.save()
        response['message'] = "Email has been updated"
        response['type'] = 'success'
    if request.POST.get('action') == "phone":
        profile = Profile.objects.get(user=request.user.pk)
        profile.phone = request.POST.get('value')
        profile.save()
        response['message'] = "Phone number has been updated"
        response['type'] = 'success'
    if request.POST.get('action') == "website":
        profile = Profile.objects.get(user=request.user.pk)
        profile.website = request.POST.get('value')
        profile.save()
        response['message'] = "Website has been updated"
        response['type'] = 'success'
    if request.POST.get('action') == "twitter":
        profile = Profile.objects.get(user=request.user.pk)
        profile.twitter = request.POST.get('value')
        profile.save()
        response['message'] = "Twitter has been updated"
        response['type'] = 'success'
    if request.POST.get('action') == "instagram":
        profile = Profile.objects.get(user=request.user.pk)
        profile.instagram = request.POST.get('value')
        profile.save()
        response['message'] = "Instagram has been updated"
        response['type'] = 'success'
    if request.POST.get('action') == "facebook":
        profile = Profile.objects.get(user=request.user.pk)
        profile.facebook = request.POST.get('value')
        profile.save()
        response['message'] = "Facebook has been updated"
        response['type'] = 'success'
    return JsonResponse(response)


def add_complain(request):
    response = dict()
    target = User.objects.get(pk=request.POST.get('user'))

    if permission_complain(request.user, target):
        Complain(user=target, complainer=request.user).save()
        response['message'] = "Thank you for complain!"
        response['type'] = "success"
    else:
        response['message'] = "You can`t add complain!"
        response['type'] = "danger"
    return JsonResponse(response)


def add_estimate(request):
    response = dict()
    target = User.objects.get(pk=request.POST.get('user'))

    if permission_estimate(request.user, target):
        Rating(user=target, ratinger=request.user, value=request.POST.get('value')).save()
        response['message'] = "Thank you for estimate!"
        response['type'] = "success"
    else:
        response['message'] = "You can`t add estimate!"
        response['type'] = "danger"
    return JsonResponse(response)


# messages

def get_contacts(request):
    response = list()
    rooms = [item.room.pk for item in RoomUser.objects.filter(user=request.user.pk)]
    companions = RoomUser.objects.filter(room__in=rooms).exclude(user=request.user.pk)
    for companion in companions:
        response.append({
            "user_id": companion.user.pk,
            "room_id": companion.room.pk,
            "name": companion.user.first_name + " " + companion.user.last_name,
            "icon": companion.user.profile.image.url if companion.user.profile.image else "",
            "new": Message.objects.filter(receiver=request.user.pk, sender=companion.user.pk, read=False).count()
        })
    return JsonResponse(response, safe=False)


@csrf_exempt
def get_messages(request):
    response = list()
    messages = Message.objects.filter(room=request.POST.get('room'))
    for message in messages:
        response.append({
            "timestamp": message.timestamp,
            "name": message.sender.first_name + " " + message.sender.last_name,
            "icon": message.sender.profile.image.url if message.sender.profile.image else "",
            "body": message.body
        })
    return JsonResponse(response, safe=False)

# ========
