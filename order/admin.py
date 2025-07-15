from django.contrib import admin
from .models import Order , OrderItem
# Register your models here.

class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    row_id_field = ("product",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id","user","updated","paid",)
    list_filter= ("paid",)
    inlines = (OrderItemInLine,)
