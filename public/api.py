from django.http import JsonResponse

from public.models import Lottery


def search_product_mini(request):
    search_text = request.POST.get('search', "")
    query = Lottery.objects.filter(name__contains=search_text)
    items = [
        {
            'id': item.pk,
            'name': item.name,
            'thumbnail': item.thumbnail.url,
            'price': item.ticket_price,
            'status': item.status
        }
        for item in query
    ]
    return JsonResponse(items, safe=False)