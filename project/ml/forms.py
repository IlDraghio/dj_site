from django import forms

class Dtc_form(forms.Form):
    criterion = forms.ChoiceField(choices=[('gini', 'gini'), ('entropy', 'entropy')], initial='gini')
    max_depth = forms.IntegerField(min_value=1, required=False)
    min_samples_split = forms.IntegerField(min_value=2, initial=2)
    min_samples_leaf=forms.IntegerField(min_value=1, initial=1)
    random_state = forms.IntegerField(min_value=0, initial=42)
    
class Knn_form(forms.Form):
    n_neighbors = forms.IntegerField(min_value=1, initial=5)
    weights = forms.ChoiceField(choices=[('uniform', 'uniform'), ('distance', 'distance')], initial='uniform')
    metric = forms.ChoiceField(choices=[('minkowski', 'minkowski'),
                                        ('euclidean', 'euclidean'),
                                        ('manhattan', 'manhattan')], initial='minkowski')
    p = forms.ChoiceField(choices=[(1, 'manhattan'), (2, 'euclidean')], initial=2)

class Svc_form(forms.Form):
    C = forms.FloatField(min_value=0.0000001, initial=1)
    kernel = forms.ChoiceField(choices=[('linear', 'linear'),
                                        ('poly', 'poly'),
                                        ('rbf', 'rbf'),
                                        ('sigmoid', 'sigmoid')], initial='rbf')
    gamma = forms.ChoiceField(choices=[('scale', 'scale'),
                                        ('auto', 'auto')], initial='auto')
    degree = forms.IntegerField(min_value=0,initial=1)
    coef0 = forms.FloatField(min_value=0.0, initial=0)
    random_state = forms.IntegerField(min_value=0, initial=42)
    
class Rfc_form(forms.Form):
    n_estimators = forms.IntegerField(min_value=2, initial=100)
    criterion = forms.ChoiceField(choices=[('gini', 'gini'), ('entropy', 'entropy')], initial='gini')
    max_depth = forms.IntegerField(min_value=1, required=False)
    min_samples_split = forms.IntegerField(min_value=2, initial=2)
    min_samples_leaf=forms.IntegerField(min_value=1, initial=1)
    max_features = forms.ChoiceField(choices=[('sqrt', 'sqrt'), ('log2', 'log2')], initial='sqrt')
    random_state = forms.IntegerField(min_value=0, initial=42)
    
class Km_form(forms.Form):
    init = forms.ChoiceField(choices=[('k-means++', 'k-means++'), ('random', 'random')], initial='k-means++')
    n_init = forms.IntegerField(min_value=1, initial=10)
    algorithm = forms.ChoiceField(choices=[('lloyd', 'lloyd'), ('elkan', 'elkan')], initial='lloyd')
    random_state = forms.IntegerField(min_value=0, initial=42)