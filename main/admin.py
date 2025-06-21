from django.contrib import admin
from .models import Client, Service, Tour

@admin.action(description="Mark as Confirmed and reward promoter")
def confirm_and_reward(modeladmin, request, queryset):
    for client in queryset:
        if client.status != 'Confirmed':
            client.status = 'Confirmed'
            client.save(update_fields=["status"])
            client.reward_promoter()  # This will handle `rewarded` flag and update promoter

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'total_price', 'ref_code', 'status')
    list_editable = ('status',)
    actions = [confirm_and_reward]

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    search_fields = ('name', 'price', 'category')
    ordering = ('name',)

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)