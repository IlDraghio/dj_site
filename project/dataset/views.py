from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .utils import mass_data_generation

@login_required(login_url="login")
def dataset_view(request):
    return render(request,'dataset/dataset.html')

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