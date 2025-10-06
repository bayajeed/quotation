from django.contrib import admin
from .models import QuotationTemplate, QuotationTemplateItem, Quotation, QuotationItem

admin.site.register(QuotationTemplate)
admin.site.register(QuotationTemplateItem)
admin.site.register(Quotation)
admin.site.register(QuotationItem)







# from django.contrib import admin
# from .models import Quotation, QuotationPart, QuotationItem

# class ItemInline(admin.TabularInline):
#     model = QuotationItem
#     extra = 0

# class PartInline(admin.TabularInline):
#     model = QuotationPart
#     extra = 0

# @admin.register(Quotation)
# class QuotationAdmin(admin.ModelAdmin):
#     list_display = ('project_name', 'client_name', 'created_at', 'total_amount_display')
#     inlines = [PartInline]  # user may instead go into parts separately

#     def total_amount_display(self, obj):
#         return obj.total_amount()
#     total_amount_display.short_description = 'Total (TK)'
