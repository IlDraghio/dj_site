from django import forms
from .models import Data

class Newdata_form(forms.ModelForm):
    class Meta:
        model = Data
        exclude = ['user','final_outcome']
        
class Massdata_form(forms.Form):
    n = forms.IntegerField(min_value=1, max_value=500, label="Number of entries to generate")
    
class Searchdata_form(forms.Form):
    name = forms.CharField(required=False, label='Name')
    surname = forms.CharField(required=False, label='Surname')
    min_age = forms.IntegerField(required=False, label='min_Age')
    max_age = forms.IntegerField(required=False, label='max_Age')
    gender = forms.ChoiceField(required=False, label='Gender',choices=[('','Any'),('Male', 'Male'), ('Female', 'Female')])
    min_weekly_study_time = forms.FloatField(required=False, label='min_WST')
    max_weekly_study_time = forms.FloatField(required=False, label='max_WST')
    min_absences = forms.IntegerField(required=False, label='min_Absences')
    max_absences = forms.IntegerField(required=False, label='max_Absences')
    min_average_grade = forms.FloatField(required=False, label='min_Av_grade')
    max_average_grade = forms.FloatField(required=False, label='max_Av_grade')
    behavior = forms.ChoiceField(required=False, label='Behavior',choices=[('','Any'),
                                                                            ('Excellent', 'Excellent'),
                                                                            ('Good', 'Good'),
                                                                            ('Sufficient', 'Sufficient'),
                                                                            ('Poor', 'Poor')])
    final_outcome =	forms.ChoiceField(required=False, label='F_outcome',choices=[('','Any'),
                                                                                ('failed', 'Failed'),
                                                                                ('passed', 'Passed')])

class Delete_data_form(forms.Form):
    id = forms.IntegerField(required=True)

class Update_data_form(forms.ModelForm):
    class Meta:
        model = Data
        exclude = ['user','id','final_outcome']