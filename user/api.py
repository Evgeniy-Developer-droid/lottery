import json

from django.http import JsonResponse
from user.Business.lottery_logic import (
    define_lottery_winners
)
from user.models import Profile


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
        print(request.FILES)
        profile = Profile.objects.get(user=request.user.pk)
        profile.image = request.FILES.get("file")
        profile.save()
        return JsonResponse({'message': "Avatar updated!", 'type':'success'})
    return JsonResponse({'message': "Something wrong with file!", 'type':'warning'})