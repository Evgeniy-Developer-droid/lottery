import json

from django.http import JsonResponse
from user.Business.lottery_logic import (
    define_lottery_winners
)


def define_winners(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if "id" not in data:
            return JsonResponse({'message': "Validation error! Set lottery id.", 'type': 'error'})
        response = define_lottery_winners(request, data)
        return JsonResponse(response, safe=False)
    return JsonResponse({'message': "Method GET not support", 'type': 'error'})
