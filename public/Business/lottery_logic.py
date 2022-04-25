from django.contrib.auth.models import User

from public.models import Lottery, Ticket, UserReview


def get_lotterys_for_catalog():
    lotterys = Lottery.objects.filter(status='active')[::-1]
    return lotterys


def get_lottery_by_id(id:int):
    try:
        lottery = Lottery.objects.get(pk=id)
    except Lottery.DoesNotExist:
        return False
    return lottery


def get_tickets_meta(id:int):
    result = {}
    lottery = Lottery.objects.get(pk=id)
    tickets = Ticket.objects.filter(lottery=id).count()
    result["purchased"] = tickets
    result["remaining"] = lottery.count_ticket - tickets
    return result


def get_reviews_by_user_id(id:int):
    return UserReview.objects.filter(destination=id)


def post_review(request, pk):
    body = request.POST.get('body', "")
    if body:
        UserReview(author=request.user, destination=User.objects.get(pk=pk), body=body).save()
        return {"message": "Create review successful.", "type": "success"}
    return {"message": "Field of review is empty.", "type": "warning"}


def get_winners_single(pk):
    return Ticket.objects.filter(lottery=pk, status='win')