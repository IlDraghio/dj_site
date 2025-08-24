from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,FileResponse
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import datetime
import io
import joblib
import base64
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
                buffer = io.BytesIO()
                joblib.dump(dtc_model, buffer)
                buffer.seek(0)
                encoded_model = base64.b64encode(buffer.read()).decode('utf-8')
                request.session['dtc_model'] = encoded_model
                messages.success(request, "DTC trained successfully!")
        elif 'export_dtc' in request.POST:
            encoded_model = request.session.get('dtc_model')
            if encoded_model:
                model_bytes = base64.b64decode(encoded_model)
                response = HttpResponse(model_bytes, content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{request.user}_dtc_model.joblib"'
                messages.success(request, "DTC model exported successfully!")
                return response
            else:
                messages.error(request, "No trained model available for export.")

        if 'knn' in request.POST:
            knn_form = Knn_form(request.POST)
            if knn_form.is_valid():
                knn_model,knn_metrics = knn(knn_form, request.user)
                request.session["knn_metrics"] = knn_metrics
                buffer = io.BytesIO()
                joblib.dump(knn_model, buffer)
                buffer.seek(0)
                encoded_model = base64.b64encode(buffer.read()).decode('utf-8')
                request.session['knn_model'] = encoded_model
                messages.success(request, "KNN trained successfully!")
        elif 'export_knn' in request.POST:
            encoded_model = request.session.get('knn_model')
            if encoded_model:
                model_bytes = base64.b64decode(encoded_model)
                response = HttpResponse(model_bytes, content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{request.user}_knn_model.joblib"'
                messages.success(request, "KNN model exported successfully!")
                return response
            else:
                messages.error(request, "No trained model available for export.")
        if 'gnb' in request.POST:
                gnb_model,gnb_metrics = gnb(request.user)
                request.session["gnb_metrics"] = gnb_metrics
                buffer = io.BytesIO()
                joblib.dump(gnb_model, buffer)
                buffer.seek(0)
                encoded_model = base64.b64encode(buffer.read()).decode('utf-8')
                request.session['gnb_model'] = encoded_model
                messages.success(request, "GNB trained successfully!")
        elif 'export_gnb' in request.POST:
            encoded_model = request.session.get('gnb_model')
            if encoded_model:
                model_bytes = base64.b64decode(encoded_model)
                response = HttpResponse(model_bytes, content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{request.user}_gnb_model.joblib"'
                messages.success(request, "GNB model exported successfully!")
                return response
            else:
                messages.error(request, "No trained model available for export.")
        if 'svc' in request.POST:
            svc_form = Svc_form(request.POST)
            if svc_form.is_valid():
                svc_model,svc_metrics = svc(svc_form, request.user)
                request.session["svc_metrics"] = svc_metrics
                buffer = io.BytesIO()
                joblib.dump(svc_model, buffer)
                buffer.seek(0)
                encoded_model = base64.b64encode(buffer.read()).decode('utf-8')
                request.session['svc_model'] = encoded_model
                messages.success(request, "SVC trained successfully!")
        elif 'export_svc' in request.POST:
            encoded_model = request.session.get('svc_model')
            if encoded_model:
                model_bytes = base64.b64decode(encoded_model)
                response = HttpResponse(model_bytes, content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{request.user}_svc_model.joblib"'
                messages.success(request, "SVC model exported successfully!")
                return response
            else:
                messages.error(request, "No trained model available for export.")        
        if 'rfc' in request.POST:
            rfc_form = Rfc_form(request.POST)
            if rfc_form.is_valid():
                rfc_model,rfc_metrics = rfc(rfc_form, request.user)
                request.session["rfc_metrics"] = rfc_metrics
                buffer = io.BytesIO()
                joblib.dump(rfc_model, buffer)
                buffer.seek(0)
                encoded_model = base64.b64encode(buffer.read()).decode('utf-8')
                request.session['rfc_model'] = encoded_model
                messages.success(request, "RFC trained successfully!")
        elif 'export_rfc' in request.POST:
            encoded_model = request.session.get('rfc_model')
            if encoded_model:
                model_bytes = base64.b64decode(encoded_model)
                response = HttpResponse(model_bytes, content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{request.user}_rfc_model.joblib"'
                messages.success(request, "RFC model exported successfully!")
                return response
            else:
                messages.error(request, "No trained model available for export.")
        if 'km' in request.POST:
            km_form = Km_form(request.POST)
            if km_form.is_valid():
                km_model,km_image = km(km_form, request.user)
                buffer = io.BytesIO()
                joblib.dump(km_model, buffer)
                buffer.seek(0)
                encoded_model = base64.b64encode(buffer.read()).decode('utf-8')
                request.session['km_model'] = encoded_model
                request.session['km_image'] = km_image
                messages.success(request, "KM segmentation success!")
        elif 'export_km' in request.POST:
            encoded_model = request.session.get('km_model')
            if encoded_model:
                model_bytes = base64.b64decode(encoded_model)
                response = HttpResponse(model_bytes, content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{request.user}_km_model.joblib"'
                messages.success(request, "KM model exported successfully!")
                return response
            else:
                messages.error(request, "No trained model available for export.")
        elif 'export_km_image' in request.POST:
            encoded_image = request.session.get('km_image')
            if encoded_image:
                image_bytes = base64.b64decode(encoded_image)
                response = HttpResponse(image_bytes, content_type='image/png')
                response['Content-Disposition'] = f'attachment; filename="{request.user}_km_plot.png"'
                return response
            else:
                messages.error(request, "No image available for export.")

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