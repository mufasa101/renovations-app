from django.contrib import admin
from.models import Service,Cost,Document,Request
# Register your models here.
@admin.register(Request)
class PostAdmin(admin.ModelAdmin):
    list_display=('name','status','priority','budget_start','budget_end')
    list_filter=('name','status','priority')
    search_fields=['name','status','priority']
    
@admin.register(Cost)
class PostAdmin(admin.ModelAdmin):
    list_display=('cost_type','cost_name','cost_total')
    list_filter=('cost_type','cost_name','cost_total')
    search_fields=['cost_type','cost_name','cost_total']
@admin.register(Document)
class PostAdmin(admin.ModelAdmin):
    list_display=('name',)
    list_filter=('name',)
    search_fields=['name']
@admin.register(Service)
class PostAdmin(admin.ModelAdmin):
    list_display=('assigned_to','status')
    list_filter=('assigned_to','status')
    search_fields=['assigned_to','status']