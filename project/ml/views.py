from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import datetime
from .utils import preprocessed_data,save_to_csv

def ml_view(request):
    return render(request,'ml/ml.html')

def preprocessed_data_view(request):
    return render(request,'preprocessed_data/preprocessed_data.html')

def preprocessed_view(request):
    data_list = preprocessed_data(request.user)
    paginator = Paginator(data_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    query_string = query_params.urlencode()
    return render(request, 'preprocessed_data/preprocessed_data.html',{'page_obj': page_obj,
                                        'query_string': query_string,}
                )

def export_csv_view(request):
    filename = f"{request.user.username}_preprocessedData_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.csv"
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return save_to_csv(request,response)