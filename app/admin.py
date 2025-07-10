from django.contrib import admin
from .models import Expense,Income
# Register your models here.
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'date')
    list_filter = ('date',)


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'date')
    list_filter = ('date',)