
from django.contrib import admin
from .models import User, Category, Expense, Group, Settlement
admin.site.register(User)

admin.site.register(Category)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'category', 'split_type', 'date', 'created_by', 'group')
    search_fields = ('amount', 'category__name', 'split_type', 'created_by__username')
    list_filter = ('category', 'split_type', 'date')

admin.site.register(Expense, ExpenseAdmin)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_type')
    search_fields = ('name',)

admin.site.register(Group, GroupAdmin)

class SettlementAdmin(admin.ModelAdmin):
    list_display = ('expense', 'payment_status', 'settlement_method', 'due_date')
    search_fields = ('expense__id', 'payment_status', 'settlement_method')
    list_filter = ('payment_status', 'settlement_method')

admin.site.register(Settlement, SettlementAdmin)


from .models import IndividualExpense

@admin.register(IndividualExpense)
class IndividualExpenseAdmin(admin.ModelAdmin):
    list_display = ('expense', 'member', 'amount', 'is_paid')
