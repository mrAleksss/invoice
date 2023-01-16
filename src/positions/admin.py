from django.contrib import admin
from .models import Position
from import_export.fields import Field
from import_export import resources
from import_export.admin import ExportActionMixin


# Register your models here.
class PositionResource(resources.ModelResource):
    description = Field()
    invoice = Field()
    
    class Meta:
        model = Position
        fields = ('id', 'invoice', 'title', 'description', 'amount', 'created')
        
    def dehydrate_description(self, obj):
        if obj.description == "":
            return "-"
        else: return obj.description
    
    def dehydrate_invoice(self, obj):
        return obj.invoice.number
        

class PositionAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = PositionResource


admin.site.register(Position, PositionAdmin)