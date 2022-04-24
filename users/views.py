from django.shortcuts import render
from django.views.generic import TemplateView
from utils import custom_apiviews,error_loop
from .models import User,AdminProfile
from .serializers import AdminProfileSerializers,RegisterSerializer
from rest_framework.response import Response
from django.contrib.postgres.search import SearchVector

# Create your views here.
class index(TemplateView):
    
    template_name = "users/index.html"

class profile(TemplateView):
    template_name = "users/profile.html"

class admin(TemplateView):
    
    template_name = "users/admin.html"

class employee(TemplateView):
    
    template_name = "users/employee.html"

class Edit_my_profile(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = AdminProfileSerializers
    queryset = AdminProfile.objects.all()
    success_update='The profile was updated'
    success_delete='The profile was deleted'
    def retrieve(self, request, *args, **kwargs):
        # instance = self.get_object()
        id=self.request.user.id
        instance = AdminProfile.objects.get(id=id)
        print("--------",instance)
        serializer = self.get_serializer(instance)
        user_data=User.objects.get(id=serializer.data['user'])
        serializer_user = RegisterSerializer(data=user_data, many=False)
        # print("heeeeeeeeeeey")
        # print(serializer_user.initial_data.email)
        return Response({
                'profile': serializer.data,
                "email":serializer_user.initial_data.email,
                "is_active":serializer_user.initial_data.is_active,
              
            })
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        profile_id=self.request.user.id
        instance = AdminProfile.objects.get(id=profile_id)
        id=instance.user.id   
        password=request.POST.get('password_credential1')   
        raw_country=request.POST.get('country_raw')
        request.data._mutable = True
        if raw_country:
            country_code = raw_country.split(',')[0]
            country = raw_country.split(',')[1]
           
            request.data['country_code']=country_code
            request.data['country']=country
        # is_active=request.POST.get('is_active')   
        print("hhhhhhhhhhh99999999999999999999999")
        print(raw_country)
        print(request.data)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            usr = User.objects.get(id=id)
            if password !="no_password":
                usr.set_password(password)
            # usr.is_active=is_active
            usr.save()
           
            return Response({
                'success': self.success_update,
                'response': serializer.data,
            })
        else:
            error_response=error_loop.fix_errors(serializer.errors)
            # error_response = fix_errors(serializer.errors.items())
            return Response({
                
                'error': error_response
            })
    def destroy(self, request, *args, **kwargs):
        # user_data=request.POST.get('user')   
        id=self.request.user.id
        instance = AdminProfile.objects.get(id=id)
        self.perform_destroy(instance)
        user_data=instance.user.id   
        u = User.objects.get(id=user_data)
        u.delete()

        return Response({
                'success': self.success_delete,
              
            })

    def perform_destroy(self, instance):
        instance.delete()
      

    def get_queryset(self):
        return AdminProfile.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class EditDelete_employee_profile(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = AdminProfileSerializers
    queryset = AdminProfile.objects.all()
    success_update='The profile was updated'
    success_delete='The profile was deleted'
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        user_data=User.objects.get(id=serializer.data['user'])
        serializer_user = RegisterSerializer(data=user_data, many=False)
        # print("heeeeeeeeeeey")
        # print(serializer_user.initial_data.email)
        return Response({
                'profile': serializer.data,
                "email":serializer_user.initial_data.email,
                "is_active":serializer_user.initial_data.is_active,
              
            })
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        id=request.POST.get('user_id')   
        password=request.POST.get('password_credential1')   
        is_active=request.POST.get('is_active')   
        print("hhhhhhhhhhh",is_active)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            usr = User.objects.get(id=id)
            if password !="no_password":
                usr.set_password(password)
            usr.is_active=is_active
            usr.save()
           
            return Response({
                'success': self.success_update,
                'response': serializer.data,
            })
        else:
            error_response=error_loop.fix_errors(serializer.errors)
            # error_response = fix_errors(serializer.errors.items())
            return Response({
                
                'error': error_response
            })
    def destroy(self, request, *args, **kwargs):
        user_data=request.POST.get('user')   
       
        instance = self.get_object()
        self.perform_destroy(instance)
        u = User.objects.get(id=user_data)
        u.delete()

        return Response({
                'success': self.success_delete,
              
            })

    def perform_destroy(self, instance):
        instance.delete()
      

    def get_queryset(self):
        return AdminProfile.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class ListCreate_employee_profile(custom_apiviews.ListBulkCreateAPIView):
    data = []
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializers
    success_insert='Your Profile has been added'
    def create(self, request, format=None, *args, **kwargs):
        request.data._mutable = True
        request.data['password']=request.POST.get('password_credential1')
        request.data['password2']=request.POST.get('password_credential2')
        request.data['username']=request.POST.get('email').split("@")[0]
        print("heeeeeeeeeeeeeeeeeeeeey",request.data)

        the_data=request.data
        many=False
      
        serializer = self.get_serializer(data=the_data, many=many)
        serializer_user = RegisterSerializer(data=the_data, many=many)
    
        if serializer.is_valid():
            if serializer_user.is_valid():
                
                saved_user = serializer_user.save(is_employee=True,is_system_admin=False,is_tenant=False,added_by=self.request.user)
                saved_profile = serializer.save(added_by=self.request.user,user=saved_user)
                
                return Response({
                    'success': self.success_insert,
                    'response': serializer.data,
                })
            else:
                error_response=error_loop.fix_errors(serializer_user.errors)
                print("serialiser USER ",error_response)
                return Response({
                    'error': error_response
                })
        else:
            error_response=error_loop.fix_errors(serializer.errors)
            print("serialiser profile ",error_response)
            return Response({
                'error': error_response
            })

    def get_queryset(self):
      
        data = AdminProfile.objects.select_related('user').filter(user__is_employee=True,user__is_system_admin=False).order_by('name')
        return data

    def filter_for_datatable(self, queryset):
   
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'name',)
            ).filter(search__icontains=search_query)
        return queryset

    def list(self, request, *args, **kwargs):
     
        draw = request.query_params.get('draw')
        queryset = self.filter_queryset(self.get_queryset())
        recordsTotal = queryset.count()
        filtered_queryset = self.filter_for_datatable(queryset)
        try:
            start = int(request.query_params.get('start'))
        except ValueError:
            start = 0
        try:
            length = int(request.query_params.get('length'))
        except ValueError:
            length = 10
        end = length + start
        data = []
        row_data = filtered_queryset[start:end]
        for row in row_data:
            if row.user.is_active:
                crede='<span class="badge light badge-success rounded">Can login</span>'
            else:
                crede='<span class="badge light badge-danger rounded">Not active</span>'
            if row.name:
                name=f'<span class="fancy_text4 fs-14">{row.name}</span>'
            else:
                name=f'<span class="fancy_text4 fs-14">{row.user.username}</span>'
            data.append([
                name,
                row.user.email,
                row.user.is_employee,
                crede,
             
               
                f'''
                <div class="dropdown float-right">
                <button type="button"
                    class="btn btn-primary light sharp btn-rounded"
                    data-toggle="dropdown" aria-expanded="false">
                    <svg width="20px" height="20px" viewBox="0 0 24 24"
                        version="1.1">
                        <g stroke="none" stroke-width="1" fill="none"
                            fill-rule="evenodd">
                            <rect x="0" y="0" width="24" height="24"></rect>
                            <circle fill="#000000" cx="5" cy="12" r="2"></circle>
                            <circle fill="#000000" cx="12" cy="12" r="2"></circle>
                            <circle fill="#000000" cx="19" cy="12" r="2"></circle>
                        </g>
                    </svg>
                </button>
                <div class="dropdown-menu" x-placement="bottom-start"
                    style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 40px, 0px);">                                                      
                   
                    <a class="dropdown-item admin_edit text-primary" id="{row.id}" >Edit</a>
                    <a class="dropdown-item admin_delete text-primary"  id="{row.id},{row.name},{row.user.id}">Delete</a>
                  

                </div>
            </div>''',
            ])
        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': filtered_queryset.count(),
            'aaData': data
        }
        return Response(response)

        
    
class EditDelete_admin_profile(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = AdminProfileSerializers
    queryset = AdminProfile.objects.all()
    success_update='The profile was updated'
    success_delete='The profile was deleted'
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        user_data=User.objects.get(id=serializer.data['user'])
        serializer_user = RegisterSerializer(data=user_data, many=False)
        if serializer_user.initial_data.is_system_admin:
            user_type="admin"
        else:
            user_type="staff"
        # print("heeeeeeeeeeey")
        # print(serializer_user.initial_data.email)
        return Response({
            
                'user_type': user_type,
                'profile': serializer.data,
                "email":serializer_user.initial_data.email,
                "is_active":serializer_user.initial_data.is_active,
              
            })
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        id=request.POST.get('user_id')   
        user_type=request.POST.get('user_type')   
        password=request.POST.get('password_credential1')   
        is_active=request.POST.get('is_active')  
        request.data._mutable = True
        print("usertype-----",user_type)
        if user_type=="admin":
            is_system_admin=True
            is_employee=False
            is_tenant=False
        elif user_type=="staff":
            is_system_admin=False
            is_employee=True
            is_tenant=False
        else:
            is_system_admin=False
            is_employee=True
            is_tenant=False

        print("hhhhhhhhhhh",user_type)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            usr = User.objects.get(id=id)
            if password !="no_password":
                usr.set_password(password)
            usr.is_system_admin=is_system_admin
            usr.is_employee=is_employee
            usr.is_tenant=is_tenant
            usr.is_active=is_active
            usr.save()
           
            return Response({
                'success': self.success_update,
                'response': serializer.data,
            })
        else:
            error_response=error_loop.fix_errors(serializer.errors)
            # error_response = fix_errors(serializer.errors.items())
            return Response({
                
                'error': error_response
            })
    def destroy(self, request, *args, **kwargs):
        user_data=request.POST.get('user')   
       
        instance = self.get_object()
        self.perform_destroy(instance)
        u = User.objects.get(id=user_data)
        u.delete()

        return Response({
                'success': self.success_delete,
              
            })

    def perform_destroy(self, instance):
        instance.delete()
      

    def get_queryset(self):
        return AdminProfile.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class ListCreate_admin_profile(custom_apiviews.ListBulkCreateAPIView):
    data = []
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializers
    success_insert='Your Profile has been added'
    def create(self, request, format=None, *args, **kwargs):
        request.data._mutable = True
        request.data['password']=request.POST.get('password_credential1')
        request.data['password2']=request.POST.get('password_credential2')
        request.data['username']=request.POST.get('email').split("@")[0]
        email=request.POST.get('email')   
        user_type=request.POST.get('user_type')   
        print("uerrrrr",user_type)
        raw_country=request.POST.get('country_raw')
        if user_type=="admin":
            print("hhhhhhhhhhere ADMIN" )
            request.data['is_system_admin']=True
            request.data['is_employee']=False
            request.data['is_tenant']=False
        elif user_type=="staff":
            print("hhhhhhhhhhere STAFF" )
            request.data['is_system_admin']=False
            request.data['is_employee']=True
            request.data['is_tenant']=False
        else:
            request.data['is_system_admin']=False
            request.data['is_employee']=True
            request.data['is_tenant']=False
        print("heeeeeeeeeeeeeeeeeeeeey",request.data)
        
        the_data=request.data
        many=False
      
        serializer = self.get_serializer(data=the_data, many=many)
        serializer_user = RegisterSerializer(data=the_data, many=many)
    
        if serializer.is_valid():
            if serializer_user.is_valid():
                
                saved_user = serializer_user.save(added_by=self.request.user)
                saved_profile = serializer.save(added_by=self.request.user,user=saved_user)
                
                return Response({
                    'success': self.success_insert,
                    'response': serializer.data,
                })
            else:
                error_response=error_loop.fix_errors(serializer_user.errors)
                print("serialiser USER ",error_response)
                return Response({
                    'error': error_response
                })
        else:
            error_response=error_loop.fix_errors(serializer.errors)
            print("serialiser profile ",error_response)
            return Response({
                'error': error_response
            })

    def get_queryset(self):
        data = AdminProfile.objects.select_related('user').order_by('name')
        # data = AdminProfile.objects.select_related('user').all().order_by('name')
        return data

    def filter_for_datatable(self, queryset):
   
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'name',)
            ).filter(search__icontains=search_query)
        return queryset

    def list(self, request, *args, **kwargs):
     
        draw = request.query_params.get('draw')
        queryset = self.filter_queryset(self.get_queryset())
        recordsTotal = queryset.count()
        filtered_queryset = self.filter_for_datatable(queryset)
        try:
            start = int(request.query_params.get('start'))
        except ValueError:
            start = 0
        try:
            length = int(request.query_params.get('length'))
        except ValueError:
            length = 10
        end = length + start
        data = []
        row_data = filtered_queryset[start:end]
        for row in row_data:
            if row.user.is_active:
                crede='<span class="badge light badge-success rounded">Can login</span>'
            else:
                crede='<span class="badge light badge-danger rounded">Not active</span>'
            if row.name:
                name=f'<span class="fancy_text4 fs-14">{row.name}</span>'
            else:
                name=f'<span class="fancy_text4 fs-14">{row.user.username}</span>'
            if  row.user.is_system_admin:
                role=f'Admin'
            elif  row.user.is_employee:
                role=f'Staff'
            else:
                role=f'----->'

            data.append([
                name,
                row.user.email,
                role,
                crede,
             
               
                f'''
                <div class="dropdown float-right">
                <button type="button"
                    class="btn btn-primary light sharp btn-rounded"
                    data-toggle="dropdown" aria-expanded="false">
                    <svg width="20px" height="20px" viewBox="0 0 24 24"
                        version="1.1">
                        <g stroke="none" stroke-width="1" fill="none"
                            fill-rule="evenodd">
                            <rect x="0" y="0" width="24" height="24"></rect>
                            <circle fill="#000000" cx="5" cy="12" r="2"></circle>
                            <circle fill="#000000" cx="12" cy="12" r="2"></circle>
                            <circle fill="#000000" cx="19" cy="12" r="2"></circle>
                        </g>
                    </svg>
                </button>
                <div class="dropdown-menu" x-placement="bottom-start"
                    style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 40px, 0px);">                                                      
                   
                    <a class="dropdown-item admin_edit text-primary" id="{row.id}" >Edit user</a>
                    <a class="dropdown-item admin_delete text-primary"  id="{row.id},{row.name},{row.user.id},{role}">Delete user</a>
                  

                </div>
            </div>''',
            ])
        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': filtered_queryset.count(),
            'aaData': data
        }
        return Response(response)

        
