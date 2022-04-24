from import_export import resources
from .models import Unit

class UnitResource(resources.ModelResource):
    class Meta:
        model = Unit