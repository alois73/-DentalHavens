from django.contrib import admin
from .models import Promoter, Code

@admin.action(description="Mark as Paid")
def mark_as_paid(modeladmin, request, queryset):
    for promoter in queryset:
        if promoter.cashout_status == 'Approved':
            promoter.cashout_status = 'Paid'
            promoter.balance = 0
            promoter.save()

@admin.action(description="Start from beginning")
def start_from_beginning(modeladmin, request, queryset):
    for promoter in queryset:
        if promoter.cashout_status == 'Paid':
            promoter.cashout_status = 'No Request'
            promoter.save()

@admin.register(Promoter)
class PromoterAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'email', 'phone', 'country', 'exp', 'tier', 'balance', 'cashout_status')
    search_fields = ('name', 'username', 'email', 'phone', 'country', 'exp', 'tier', 'balance', 'cashout_status')
    list_editable = ('cashout_status',)
    actions = [mark_as_paid, start_from_beginning]

@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ('ref_code', 'user')
    search_fields = ('ref_code', 'user__name', 'user__email')
    list_filter = ('user__tier',)