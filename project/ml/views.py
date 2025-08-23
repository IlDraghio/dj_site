from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,FileResponse
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import datetime
from .utils import preprocessed_data,save_to_csv,dtc,knn,gnb,svc,rfc,km
from .forms import *

def ml_view(request):
    dtc_form = Dtc_form()
    dtc_metrics = request.session.get("dtc_metrics")
    knn_form = Knn_form()
    knn_metrics = request.session.get("knn_metrics")
    #no hyperparameters for GaussianNB
    gnb_metrics = request.session.get("gnb_metrics")
    svc_form = Svc_form()
    svc_metrics = request.session.get("svc_metrics")
    rfc_form = Rfc_form()
    rfc_metrics = request.session.get("rfc_metrics")
    km_form = Km_form()
    km_image = request.session.get("km_image")
    
    if request.method == 'POST':
        if 'dtc' in request.POST:
            dtc_form = Dtc_form(request.POST)
            if dtc_form.is_valid():
                dtc_model,dtc_metrics = dtc(dtc_form, request.user)
                request.session["dtc_metrics"] = dtc_metrics
                messages.success(request, "Decision Tree trained successfully!")
        elif 'knn' in request.POST:
            knn_form = Knn_form(request.POST)
            if knn_form.is_valid():
                knn_metrics = knn(knn_form, request.user)
                request.session["knn_metrics"] = knn_metrics
                messages.success(request, "KNN trained successfully!")
        elif 'gnb' in request.POST:
                gnb_metrics = gnb(request.user)
                request.session["gnb_metrics"] = gnb_metrics
                messages.success(request, "GNB trained successfully!")
        elif 'svc' in request.POST:
            svc_form = Svc_form(request.POST)
            if svc_form.is_valid():
                svc_metrics = svc(svc_form, request.user)
                request.session["svc_metrics"] = svc_metrics
                messages.success(request, "SVC trained successfully!")
        elif 'rfc' in request.POST:
            rfc_form = Rfc_form(request.POST)
            if rfc_form.is_valid():
                rfc_metrics = rfc(rfc_form, request.user)
                request.session["rfc_metrics"] = rfc_metrics
                messages.success(request, "RFC trained successfully!")
        elif 'km' in request.POST:
            km_form = Km_form(request.POST)
            if km_form.is_valid():
                km_image = km(km_form, request.user)
                messages.success(request, "KM segmented successfully!")
                
    return render(request, 'ml/ml.html', {
        'dtc_form': dtc_form,
        'dtc_metrics': dtc_metrics,
        'knn_form': knn_form,
        'knn_metrics': knn_metrics,
        #no form for GaussianNB
        'gnb_metrics': gnb_metrics,
        'svc_form': svc_form,
        'svc_metrics': svc_metrics,
        'rfc_form': rfc_form,
        'rfc_metrics': rfc_metrics,
        'km_form': km_form,
        'km_image': km_image,
    })

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