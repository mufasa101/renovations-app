from django.shortcuts import  HttpResponse
from property.models import Unit
from django.db.models import Q
from users.models import User
import json
def units(request):
    status = request.GET.get('status',None) 
    except_unit = request.GET.get('unit',None) 
    user=request.user
    is_system_admin=request.user.is_system_admin
    data=Unit.objects.select_option_units(status=status,user=user,is_system_admin=is_system_admin,except_unit=except_unit)
    return HttpResponse(data)
# def contractor(request):
#     status = request.GET.get('status',None) 
#     except_unit = request.GET.get('unit',None) 
#     user=request.user
#     is_system_admin=request.user.is_system_admin
#     data=Unit.objects.select_option_units(status=status,user=user,is_system_admin=is_system_admin,except_unit=except_unit)
#     return HttpResponse(data)

def contractor(request):
    
    data = User.objects.filter(Q(is_employee=True)|Q(is_system_admin=True))
    output= []
    for row in data:

        name=row.username
        output.append(f'<option " value="{row.id}">{name} </option>')        
    return HttpResponse(output)