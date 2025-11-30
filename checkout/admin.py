from django.contrib import admin
from .models import Order, OrderDetails


class OrderDetailsAdminInline(admin.TabularInline):
    model = OrderDetails


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderDetailsAdminInline,)

    readonly_fields = ('date_ordered',
                       'grand_total',)

    fields = ('appointment', 'date_ordered', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'grand_total',)

    list_display = ('date_ordered', 'appointment', 'full_name',
                    'grand_total',)

    ordering = ('-date_ordered',)

admin.site.register(Order, OrderAdmin)