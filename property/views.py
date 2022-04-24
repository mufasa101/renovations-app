from re import L
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from utils import custom_apiviews,error_loop
from rest_framework.response import Response
from utils.bulk_insert import bulk_data_fomart_decision,bulk_data_fomart_receipt
from .serializers import UnitSerializers,Unit
from django.contrib.postgres.search import SearchVector
from django.db.models import Q,Sum

# Create your views here.
class Index(TemplateView):
    
    template_name = "property/index.html"

    def get_context_data(self, **kwargs):
        from services.models import Request,Service,Cost
        if self.request.user.is_system_admin:
            projects= Request.objects.all().order_by('assigned_to')
            incomplete_tasks=Service.objects.filter(~Q(status='complete'))
            actual_budget=Cost.objects.aggregate(amount=Sum('cost_total'))
        else:
            projects= Request.objects.filter(assigned_to=self.request.user).order_by('assigned_to')
            incomplete_tasks=Service.objects.filter(~Q(status='complete'),Q(assigned_to=self.request.user))
        actual_budget=Cost.objects.filter(maintenance__assigned_to=self.request.user).aggregate(amount=Sum('cost_total'))
        ganttchart={}
        tasks={}

        # ganttchart['john']={'lauundrey':5,'kitched':18}
        # ganttchart['jack']={'cleaning':5}


        context = super().get_context_data(**kwargs)
        
        incomplete_projects=projects.filter(~Q(status='complete'))
        context['projects'] = incomplete_projects
        context['incomplete_tasks'] = incomplete_tasks
        context['complete'] = projects.filter(Q(status='complete')).count()
        context['in_progress'] = projects.filter(Q(status='in progress')).count()
        context['not_started'] = projects.filter(Q(status='not started')).count()
        context['planned_budget'] = projects.aggregate(amount=Sum('budget_amount'))
        context['actual_budget'] = actual_budget
        current="none"
        past="none_past"
        print("0-----------")
   
        for r in incomplete_projects:
            print("current:",current,"past:",past)
            current=r.assigned_to.profile_user.name
            # tasks[f'{r.category}']=r.budget_start
            if current == past:
                tasks[f'{r.category},{r.budget_start},{r.budget_end} ']=f'{r.budget_start},{r.budget_end} '
                ganttchart[f'{current}']=tasks
                
                # tasks={}
            else:
                print("Not equal")
               
                # ganttchart[f'{past}']=tasks
                
            
                tasks={}
                tasks[f'{r.category},{r.budget_start},{r.budget_end} ']=f'{r.budget_start},{r.budget_end} '
                ganttchart[f'{current}']=tasks
            past=r.assigned_to.profile_user.name
        context['ganttchart'] = ganttchart


        return context



class Add(TemplateView):
    
    template_name = "property/add.html"

 
class EditDelete_property(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = UnitSerializers
    queryset = Unit.objects.all()
    success_update='The unit was updated'
    success_delete='The unit was deleted'
   
    def get_queryset(self):  
        
        return Unit.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        request.data._mutable = True 
        raw_data=request.POST.get('unit_type_raw')
        unit_type = raw_data.split(',')[0]
        unit_category = raw_data.split(',')[1]
        request.data['unit_type']=unit_type
        request.data['unit_category']=unit_category

        if self.request.user.is_system_admin:
            # request.data['owned_by']=request.POST.get('owned_by')
            request.data['owned_by']=self.request.user.id
        else:
            request.data['owned_by']=self.request.user.id

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response({
                'success': self.success_update,
                'response': serializer.data,
              
            })
        else:
            error_response =  error_loop.fix_errors(serializer.errors)
            return Response({
                
                'error': error_response
            })

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class ListCreate_property(custom_apiviews.ListBulkCreateAPIView):

    data = []
    queryset = Unit.objects.all()
    serializer_class = UnitSerializers
    success_insert='Your unit has been added'
    def create(self, request, format=None, *args, **kwargs):
        request.data._mutable = True
        raw_data=request.POST.get('unit_type_raw')
        unit_type = raw_data.split(',')[0]
        unit_category = raw_data.split(',')[1]
        request.data['unit_type']=unit_type
        request.data['unit_category']=unit_category

        if self.request.user.is_system_admin:
            # request.data['owned_by']=request.POST.get('owned_by')
            request.data['owned_by']=self.request.user.id
        else:
            request.data['owned_by']=self.request.user.id
      
        the_data=request.data
        many=False
        serializer = self.get_serializer(data=the_data, many=many)
        if serializer.is_valid():

            saved_user2 = serializer.save(added_by=self.request.user)

            property_auto= serializer.data['id']
            property_name= request.POST.get('unit_number')
            return Response({
                'property_auto': property_auto,
                'property_name': property_name,
               
                'success': self.success_insert,
                # 'response': serializer.data,
            })
        else:
            error_response = error_loop.fix_errors(serializer.errors)
            print("serialiser errors",serializer.errors)
            return Response({
                'error': error_response
            })

    def get_queryset(self):
        if self.request.user.is_system_admin:
            data=Unit.objects.all().order_by('unit_number')
        else:
            data=Unit.objects.filter(owned_by=self.request.user).order_by('unit_number')
        return data

    def filter_for_datatable(self, queryset):
   
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                   'unit_number',)
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
           data.append ([
                
                f'''   
                {row.property_name}<br>
               Unit #{row.unit_number}
            
                ''',
            row.unit_type,
            f' {row.state}, {row.city} ',
            f' <span class="text-right fancy_text4">{row.monthly_net_increase} </span> ',
            f' <span class="text-right fancy_text4">{row.annualized_increase} </span> ',

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
                       
                        <a class="dropdown-item edit_property_button text-primary" id="{row.id}">Edit</a>
                        <a class="dropdown-item delete_property_button text-primary" id="Unit {row.unit_number},{row.id}">Delete</a>
                         

                    </div>
                </div>
               ''',
               
             
            ])
        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': filtered_queryset.count(),
            'aaData': data
        }
        return Response(response)
    

from tablib import Dataset
from .resources import UnitResource
class ListCreate_property_excel(custom_apiviews.ListBulkCreateAPIView):

    data = []
    queryset = Unit.objects.all()
    serializer_class = UnitSerializers
    success_insert='Your file has been uploaded'
    def create(self, request, format=None, *args, **kwargs):
        import_resource = UnitResource()
        dataset = Dataset()
        new_persons = request.FILES['excel_document']
        imported_data = dataset.load(new_persons.read(),format='xlsx')
        result = import_resource.import_data(dataset, dry_run=True)  # Test the data import
        last_id=Unit.objects.latest('id').id
        id=last_id+1
        for data in imported_data:
            print(data[1])
            print("id-----",id)
            if data[1]:
                print(data)
                Unit.objects.create(id=id, property_name=data[0],unit_number=data[1],unit_category=data[2],unit_type=data[3]
                ,move_out_date=data[4]
                ,made_ready_date=data[5]
                ,move_in_date=data[6]
                ,priror_rent=data[7]
                ,net_renovated_rent=data[8]
                ,monthly_net_increase=data[9]
                ,annualized_increase=data[10]
                ,comments=data[11]
                ,added_by=self.request.user
                ,added_through='excel')
                id+=1
            else:
                break
        return Response({
    
            
            'success': self.success_insert,
            # 'response': serializer.data,
        })
        # else:
        #     error_response = error_loop.fix_errors(serializer.errors)
        #     print("serialiser errors",serializer.errors)
        #     return Response({
        #         'error': error_response
        #     })

    def get_queryset(self):
        if self.request.user.is_system_admin:
            data=Unit.objects.filter(added_through="excel").order_by('-added_on')
        else:
            data=Unit.objects.filter(owned_by=self.request.user,added_through="excel").order_by('-added_on')
        return data

    def filter_for_datatable(self, queryset):
   
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                   'unit_number',)
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
           data.append ([
                
                f'''   
                {row.property_name}<br>
               Unit #{row.unit_number}
            
                ''',
            row.unit_type,
            f' {row.state}, {row.city} ',
            f' <span class="text-right fancy_text4">{row.monthly_net_increase} </span> ',
            f' <span class="text-right fancy_text4">{row.annualized_increase} </span> ',
            f' <span class="text-right fancy_text4 text-success">Excel </span> ',
            F'<a class="btn btn-outline-danger px-4 btn-rounded py-1 delete_property_button" id="Unit {row.unit_number},{row.id}">Delete</a>'
     
               
             
            ])
        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': filtered_queryset.count(),
            'aaData': data
        }
        return Response(response)
    
from tablib import Dataset
from .resources import UnitResource
def import_property(request):
    if request.method == 'POST':
        print("----------------------------POST")
        person_resource = UnitResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']
        imported_data = dataset.load(new_persons.read(),format='xlsx')

        # imported_data = dataset.load(new_persons.read())
        result = person_resource.import_data(dataset, dry_run=True)  # Test the data import
        print(new_persons.read())
        last_id=Unit.objects.latest('id').id
        id=last_id+1
        print("------------------no errors")
        # if not result.has_errors():
        for data in imported_data:
            print(data[1])
            print("id-----",id)
            if data[1]:
                print(data)
                Unit.objects.create(id=id, property_name=data[0],unit_number=data[1],unit_category=data[2],unit_type=data[3]
                
                ,move_out_date=data[4]
                ,made_ready_date=data[5]
                ,move_in_date=data[6]
                ,priror_rent=data[7]
                ,net_renovated_rent=data[8]
                ,monthly_net_increase=data[9]
                ,annualized_increase=data[10]
                ,comments=data[11]
                ,added_through='excel'
                
                
                
                )
                # value = Unit(
                #     id,
                #     property_name=data[0],
                #     data[1],
                #     data[2],
                #     data[4],
                #     data[5],
                #     data[6],
                #     data[7],
                #     )
                # value.save()
                id+=1
            else:
                break
            # print("errrroorrrs,",result.has_errors())
            # person_resource.import_data(dataset, dry_run=False)  

    return render(request, 'property/import.html')

def test(request):
    
    last_id=Unit.objects.latest('id')
    print("--------------")
    print("-------------last id",last_id.id)
    j=0
    for i in range(6):
        print(i)
        j+=2
        print("j---",j)