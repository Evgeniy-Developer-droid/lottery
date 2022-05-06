import datetime
import time
from celery import shared_task
from celery.utils.log import get_task_logger
from public.models import Lottery


logger = get_task_logger(__name__)


@shared_task
def canceled_lottery():
    one_day_ago = datetime.datetime.today() - datetime.timedelta(1)
    lottery = Lottery.objects.filter(status='active', finish__lt=one_day_ago)
    for obj in lottery:
        obj.status = 'canceled'
        obj.save()
    # lottery.update(status='canceled')
