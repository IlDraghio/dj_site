from django.db import models
from django.contrib.auth.models import User

class Preprocessed_data(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,default="")
    age = models.FloatField(default=0)
    weekly_study_time = models.FloatField(default=0)
    absences = models.FloatField(default=0)
    average_grade = models.FloatField(default=0)
    behavior = models.FloatField(default=0)
    final_outcome =	models.CharField(default="")
    gender_Male = models.FloatField(default=0)

