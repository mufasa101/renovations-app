from django.urls import reverse
from django.views.generic import TemplateView
from utils import custom_apiviews,error_loop
from rest_framework.response import Response
from utils.bulk_insert import bulk_data_fomart_decision,bulk_data_fomart_receipt
from .serializers import RequestSerializers,Request,Cost,CostSerializers,Document,DocumentSerializers,Service,ServiceSerializers
from django.contrib.postgres.search import SearchVector
from django.shortcuts import get_object_or_404

# Create your views here.
class Index(TemplateView):
    template_name = "services/index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        show_add_modal=self.request.GET.get('modal', "")
        if show_add_modal:
            context['modal'] = show_add_modal
        print("------",context)
        return context

class details(TemplateView):
    
    template_name = "services/details.html"
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['main'] = get_object_or_404(Request, pk=self.kwargs.get('maintenance'))
        
            return context

class EditDelete_service(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    success_update='The record was updated successfully'
    success_delete='The record was deleted successfully'
    serializer_class = ServiceSerializers
    queryset = Service.objects.all()
    def get_queryset(self):
        return Service.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class ListCreate_service(custom_apiviews.ListCreateAPIView):
    data = []
    queryset = Service.objects.all()
    serializer_class = ServiceSerializers
    success_insert='The record has been added'

    def get_queryset(self):
        maintenance=self.request.query_params.get('maintenance')
        if self.request.user.is_system_admin:
            data = Service.objects.filter(maintenance=maintenance)
        else:
            data = Service.objects.filter(assigned_to=self.request.user,maintenance=maintenance)
        
        return data

    def filter_for_datatable(self, queryset):
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'action_title', 'status')
            ).filter(search__icontains=search_query)
        return queryset

    def list(self, request, *args, **kwargs):
        draw = request.query_params.get('draw')
        queryset = self.filter_queryset(self.get_queryset())
        recordsTotal = queryset.count()
        row_data = self.filter_for_datatable(queryset)
        data = []

        for row in row_data:
            status=f'<span class="badge light badge-success btn-rounded px-4">Complete</span>'
            if row.status=="in progress":
                status=f'<span class="badge light badge-primary btn-rounded px-4">In progress</span>'
            if row.status=="not started":
                status=f'<span class="badge light badge-danger btn-rounded px-4">Not started</span>'
            if row.arrived=="yes":
                    date_data= f'''          
                    Arrived on:<br>{row.date_in.strftime("%d %B, %Y")} 
                    '''


            else:
                date_data= f'''          
                Scheduled for: <br>{row.scheduled_date.strftime("%d %B, %Y")}  
                    '''
            name=row.assigned_to.username
            data.append([
                
               name,
               date_data,
               
                status,
              
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
                 
                    <a class="dropdown-item edit_service " id="{row.id}" >Edit</a>
                    <a class="dropdown-item remove_service" id="{row.id},{name}" >Delete</a>
                      <hr>
       
                  
                </div>
            </div>''',
            
              
            ])
        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': row_data.count(),
            'aaData': data
        }
        return Response(response)
class EditDelete_request(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    success_update='The record was updated successfully'
    success_delete='The record was deleted successfully'
    serializer_class = RequestSerializers
    queryset = Request.objects.all()
    def get_queryset(self):
        return Request.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class ListCreate_request(custom_apiviews.ListCreateAPIView):
    data = []
    queryset = Request.objects.all()
    serializer_class = RequestSerializers
    success_insert='The record has been added'

    def get_queryset(self):
        if self.request.user.is_system_admin:
            data = Request.objects.all()
        else:
            data = Request.objects.filter(assigned_to=self.request.user).select_related('unit')


        return data

    def filter_for_datatable(self, queryset):
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'name', 'status')
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

        if not request.user.is_system_admin:
            class_variable="d-none"
        else:
            class_variable="hello-world"
        for row in row_data:
            status=f'<span class="badge light badge-success btn-rounded px-4">Complete</span>'
            if row.status=="in progress":
                status=f'<span class="badge light badge-primary btn-rounded px-4">In progress</span>'
            if row.status=="not started":
                status=f'<span class="badge light badge-danger btn-rounded px-4">Not started</span>'
            if row.reported_on:
                reported_on= f'''          
                   {row.reported_on.strftime("%Y-%m-%d")}<br>{row.since} days ago
                  '''
            else:
                reported_on="---------"
            
            data.append([
                row.unit.property_name,
                f' {row.unit.property_name} <br> unit {row.unit.unit_number}',
                row.name,
                reported_on,
              f'''          
                   Budget cost:{row.budget_amount}
                     <br>
                  Days to complete:{row.budget_days}
                 
                   
                  ''',
                status,
                          
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
                 
                    <a class="dropdown-item edit_maintenance " id="{row.id}" >Edit</a>
                    <a class="dropdown-item remove_maintenance  {class_variable}" id="{row.id},{row.name}" >Delete</a>
                      <hr>
                    <a class="dropdown-item cost_button {class_variable}" id="{row.id}" >View costs</a>
                    <a class="dropdown-item service_button {class_variable}" id="{row.id}" >View tasks</a>
                    <a class="dropdown-item attach_photos" id="{row.id}" >View photos/videos</a>
      
                  
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

class EditDelete_cost(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    success_update='The cost was updated successfully'
    success_delete='The cost was deleted successfully'
    serializer_class = CostSerializers
    queryset = Cost.objects.all()
    def get_queryset(self):
        return Cost.objects.all()
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class ListCreate_cost(custom_apiviews.ListCreateAPIView):
    data = []
    queryset = Cost.objects.all()
    serializer_class = CostSerializers
    success_insert='The cost has been added'
    def get_queryset(self):
        maintenance=self.request.query_params.get('maintenance')
        data = Cost.objects.filter(maintenance=maintenance).order_by('added_on')
        return data

    def filter_for_datatable(self, queryset):
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'cost_type', 'cost_name', 'paid_by')
            ).filter(search__icontains=search_query)
        return queryset

    def list(self, request, *args, **kwargs):
        draw = request.query_params.get('draw')
        queryset = self.filter_queryset(self.get_queryset())
        recordsTotal = queryset.count()
        row_data = self.filter_for_datatable(queryset)
        data = []
        for row in row_data:
            data.append([
                   f'''          
            {row.cost_type}<br>({row.cost_name})
                  ''',
                row.cost_total,
                row.paid,
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
                    <a class="dropdown-item edit_cost text-primary" id="{row.id}" >Edit</a>
                    <a class="dropdown-item remove_cost text-primary" id="{row.id},{row.maintenance.id}" >Delete</a>
                </div>
            </div>''',
            
              
            ])
        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': row_data.count(),
            'aaData': data
        }
        return Response(response)

       
class EditDelete_document(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    success_update='The photo was updated successfully'
    success_delete='The photo was deleted successfully'
    serializer_class = DocumentSerializers
    queryset = Document.objects.all()
    def get_queryset(self):
        return Document.objects.all()
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}
class ListCreate_document(custom_apiviews.ListCreateAPIView):
    data = []
    queryset = Document.objects.all()
    serializer_class = DocumentSerializers
    success_insert='The photo has been added'
    def get_queryset(self):
        maintenance=self.request.query_params.get('maintenance')
        data = Document.objects.filter(maintenance=maintenance).order_by('added_on')
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
        row_data = self.filter_for_datatable(queryset)
        data = []
        for row in row_data:
            if row.category =="photo":
                download=f'<a class="dropdown-item download_document " href="{row.photo.url}" id="{row.id}" >Download</a>'
                doc=f'<img src="{row.photo.url}" alt="unit photo" style="width:60px;height:40px;border:2px solid #3B4CB8;">'
            else:
                doc=f'<a style="border-bottom:2px solid grey" class="fancy_text5 text-primary border-primary pb-1" href="{row.video}">View video</a>'
                download=''
            data.append([
                doc,
                row.category,
                row.name,
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
                   {download}
                    <a class="dropdown-item remove_document" id="{row.id},{row.maintenance.id}" >Delete</a>
                </div>
            </div>''',
            
              
            ])
        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': row_data.count(),
            'aaData': data
        }
        return Response(response)
