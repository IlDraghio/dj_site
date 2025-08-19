from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

class Data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 20)
    surname = models.CharField(max_length = 20)
    age = models.PositiveIntegerField(validators=[MinValueValidator(14),MaxValueValidator(20)])
    gender = models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')])
    weekly_study_time = models.FloatField(validators=[MinValueValidator(0.0)])
    absences = models.PositiveIntegerField(validators=[MaxValueValidator(300)])
    average_grade = models.FloatField(validators=[MinValueValidator(4),MaxValueValidator(10)])
    behavior = models.CharField(choices=[('Excellent', 'Excellent'),
                                                        ('Good', 'Good'),
                                                        ('Sufficient', 'Sufficient'),
                                                        ('Poor', 'Poor')])
    final_outcome =	models.CharField()
    
    def save(self, *args, **kwargs):  # Override save() to define final_outcome based on other fields
        if self.average_grade <= 5.3 or self.absences >= 220 or self.behavior == 'Poor':
            self.final_outcome = 'failed'
        else:
            self.final_outcome = 'passed'

        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"User: {self.user.id} - data_id: {self.id}"