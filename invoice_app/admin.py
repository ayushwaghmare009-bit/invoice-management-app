from django.contrib import admin
from .models import invoice

class InvoiceAdmin(admin.ModelAdmin):
    list_display=[
        'invoice_number','customer_name','amount','date_created','is_paid'
    ]
    search_fields = ['customer_name','invoice_number']
    list_filter=['is_paid','date_created']
    ordering=['-date_created']

admin.site.register(invoice,InvoiceAdmin)

