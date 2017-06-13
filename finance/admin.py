from django.contrib import admin
from .models import Finance
# Register your models here.

class FinanceAdmin(admin.ModelAdmin):
	list_display = ('id', 'out_trade_no',  'trade_status', 'products', 'user', 'total_amount', 'timestamp')


admin.site.register(Finance, FinanceAdmin)
