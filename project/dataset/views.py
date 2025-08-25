from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import csv
from .forms import *
from .utils import mass_data_generation,search_data
from .models import Data

@login_required(login_url="login")
def dataset_view(request):
    current_user = request.user
    search_data_form = Searchdata_form(request.GET or None)
    data_list = Data.objects.filter(user=current_user).order_by('id')
    if search_data_form.is_valid():
        data_list = search_data(search_data_form,data_list)
    paginator = Paginator(data_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    query_string = query_params.urlencode()
    return render(request, 'dataset/dataset.html', {
                                                    'search_data_form': search_data_form,
                                                    'page_obj': page_obj,
                                                    'query_string': query_string,}
                )

@login_required(login_url="login")
def newdata_view(request):
    if request.method == 'POST':
        
        if 'new_data' in request.POST:
            new_data_form = Newdata_form(request.POST)
            if new_data_form.is_valid():
                instance = new_data_form.save(commit=False)
                instance.user = request.user
                instance.save()
                messages.success(request, 'Student added successfully!')
                return redirect('new_data')
            
        elif 'mass_data' in request.POST:
            massdata_form = Massdata_form(request.POST)
            if massdata_form.is_valid():
                n = massdata_form.cleaned_data['n']
                mass_data_generation(request,n)
                messages.success(request, f'{n} students added succesfully!')
                return redirect('new_data')
    else:
        new_data_form = Newdata_form()
        massdata_form = Massdata_form()
        
    return render(request,'new_data/new_data.html',{'new_data_form': new_data_form, 
                                                    'mass_data_form': massdata_form})

@login_required(login_url="login")
def massdata_view(request):
    if request.method == 'POST':
        massdata_form = Massdata_form(request.POST)
        if massdata_form.is_valid():
            n = massdata_form.cleaned_data['n']
            mass_data_generation(request,n)
            messages.success(request, f'{n} students added succesfully!')
        return redirect('new_data')
    else:
        massdata_form = Massdata_form()

    return render(request, 'partials/mass_data.html', {'form': massdata_form})

def delete_data_view(request):
    if request.method == 'POST':
        pk = request.POST.get('id_to_delete')
        try:
            data = get_object_or_404(Data, pk=pk)
            data.delete()
            messages.success(request, 'Student deleted successfully!')
        except Exception as e:
            messages.error(request, 'No data found with that ID.')
        return redirect('dataset')
    return render(request, 'dataset/dataset.html')

def update_data_view(request):
    pk = request.GET.get('id') or request.POST.get('id')
    if not pk:
        messages.error(request, 'No ID provided.')
        return redirect('dataset')
    
    try:
        data = get_object_or_404(Data, pk=pk)
    except Exception as e:
        messages.error(request, 'No data found with that ID.')
        return redirect("dataset")
        
    if request.method == 'POST' and 'id_to_update' not in request.POST:
        update_form = Update_data_form(request.POST, instance=data)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, "Data updated successfully!")
            return redirect('dataset')
    else:
        update_form = Update_data_form(instance=data)
    return render(request, 'update_data/update_data.html', {'update_form': update_form, 'data': data})

def import_csv_view(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
        except Exception as e:
            messages.error(request, f"{e} Failed to decode CSV file.")
            return redirect('new_data')
        
        for row in reader:
            try:
                Data.objects.create(
                    user = request.user,
                    name = row["name"],
                    surname = row["surname"],
                    age = int(row["age"]),
                    gender = row["gender"],
                    weekly_study_time = float(row["weekly_study_time"]),
                    absences = int(row["absences"]),
                    average_grade = float(row["average_grade"]),
                    behavior = row["behavior"],
                    final_outcome =	row["final_outcome"],
                )
            except Exception as e:
                messages.error(request, f"{e} Failed to decode CSV file.")
                return redirect('new_data')
        messages.success(request, "CSV imported successfully.")
        return redirect('new_data')

    return render(request, 'partials/import_csv.html')

def export_csv_view(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dataset.csv"'

    writer = csv.writer(response)
    writer.writerow(['name','surname','age','gender','weekly_study_time','absences','average_grade','behavior','final_outcome'])

    for data in Data.objects.filter(user=request.user):
        writer.writerow([data.name,
                        data.surname,
                        data.age,
                        data.gender,
                        data.weekly_study_time,
                        data.absences,
                        data.average_grade,
                        data.behavior,
                        data.final_outcome])
    return response