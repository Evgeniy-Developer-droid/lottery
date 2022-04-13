from django.contrib import admin
from .models import AdminSetting, Transaction


@admin.register(Transaction)
class TransactionView(admin.ModelAdmin):
    list_display = ("payment_id", "order_id", "amount", "currency", "status", "timestamp",)

@admin.register(AdminSetting)
class AdminSettingView(admin.ModelAdmin):

    def has_add_permission(self, request):
        retVal = super().has_add_permission(request)
        if retVal and AdminSetting.objects.exists():
            retVal = False
        return retVal
