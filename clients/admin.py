# clients/admin.py
from django.contrib import admin

from .models import Loan

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('client', 'amount', 'approved', 'created_at')
    list_filter = ('approved', 'created_at')
    search_fields = ('client__full_name',)
