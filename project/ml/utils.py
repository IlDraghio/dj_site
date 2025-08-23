from django.http import Http404
from django.contrib.auth.models import User
from dataset.models import Data
from .models import Preprocessed_data
import pandas as pd
import csv
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import io
import base64


def queryset_to_df(user):
    queryset = Data.objects.filter(user=user)
    return pd.DataFrame(list(queryset.values()))

def drop_irr_columns(df):
    return df.drop(columns=['id','name','surname'])

def encode_labels(df):
    encoders = {}
    columns = ['behavior','final_outcome']
    for c in columns:
        le = LabelEncoder()
        df[c] = le.fit_transform(df[c])
        encoders[c] = le 
    return df, encoders

def one_hot_labels(df):
    ohe = OneHotEncoder(sparse_output=False, drop='first')
    encoded_data = ohe.fit_transform(df[["gender"]])       
    encoded_cols = ohe.get_feature_names_out(["gender"])   
    df_encoded = pd.DataFrame(encoded_data, columns=encoded_cols, index=df.index)
    df_final = pd.concat([df.drop(columns="gender"), df_encoded], axis=1)
    return df_final,ohe

def normalize_data(df):
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.difference(['user_id',"gender_Male",'behavior','final_outcome'])
    scaler = StandardScaler()
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])
    return df,scaler

def split_data(df):
    X = df.drop(columns=["final_outcome"])
    y = df["final_outcome"]
    X_train,X_test, y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)
    return X_train,X_test, y_train,y_test

def preprocessed_data(user):
    df_pure = queryset_to_df(user)
    df = drop_irr_columns(df_pure)
    df,le = encode_labels(df)
    df,ohe = one_hot_labels(df)
    df,ss = normalize_data(df)
    print(df.describe())
    pre_data = [
    Preprocessed_data(
        user_id = User.objects.get(id=int(row['user_id'])),
        age = row['age'],
        weekly_study_time = row['weekly_study_time'],
        absences = row['absences'],
        average_grade = row['average_grade'],
        behavior = row['behavior'],
        final_outcome =	row['final_outcome'],
        gender_Male = row['gender_Male'],
        )
    for _, row in df.iterrows()
    ]
    Preprocessed_data.objects.all().delete()
    Preprocessed_data.objects.bulk_create(pre_data)
    return Preprocessed_data.objects.filter(user_id=user)

def save_to_csv(request,response):
    writer = csv.writer(response)
    writer.writerow(['age','gender_Male','weekly_study_time','absences','average_grade','behavior','final_outcome'])
    for data in Preprocessed_data.objects.filter(user_id=request.user):
        writer.writerow([data.age,
                        data.gender_Male,
                        data.weekly_study_time,
                        data.absences,
                        data.average_grade,
                        data.behavior,
                        data.final_outcome])
    return response

def get_preprocessed_df(user):
    queryset = Preprocessed_data.objects.filter(user_id=user)
    df = pd.DataFrame.from_records(queryset.values('age', 'weekly_study_time', 'absences',
        'average_grade', 'behavior', 'final_outcome', 'gender_Male'
    ))
    return df

def compute_metrics(y_test, y_pred):
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    return {
        'accuracy': acc,
        'confusion_matrix': cm.tolist(),
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }

def dtc(dtc_form,user):
    dtc = DecisionTreeClassifier(
        criterion=dtc_form.cleaned_data['criterion'],
        max_depth=dtc_form.cleaned_data['max_depth'],
        min_samples_split=dtc_form.cleaned_data['min_samples_split'],
        min_samples_leaf=dtc_form.cleaned_data['min_samples_leaf'],
        random_state=dtc_form.cleaned_data['random_state']
    )
    df = get_preprocessed_df(user)
    X_train,X_test, y_train,y_test = split_data(df)
    dtc.fit(X_train, y_train)
    y_pred = dtc.predict(X_test)
    return dtc,compute_metrics(y_test, y_pred)

def knn(knn_form,user):
    knn = KNeighborsClassifier(
        n_neighbors=knn_form.cleaned_data['n_neighbors'],
        weights=knn_form.cleaned_data['weights'],
        metric=knn_form.cleaned_data['metric'],
        p= float(knn_form.cleaned_data['p'])
    )
    df = get_preprocessed_df(user)
    X_train,X_test, y_train,y_test = split_data(df)
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    return compute_metrics(y_test, y_pred)

def gnb(user):
    gnb = GaussianNB()
    df = get_preprocessed_df(user)
    X_train,X_test, y_train,y_test = split_data(df)
    gnb.fit(X_train, y_train)
    y_pred = gnb.predict(X_test)
    return compute_metrics(y_test, y_pred)

def svc(svc_form,user):
    svc = SVC(
        C=svc_form.cleaned_data['C'],
        kernel=svc_form.cleaned_data['kernel'],
        gamma=svc_form.cleaned_data['gamma'],
        degree= int((svc_form.cleaned_data['degree'])),
        coef0= svc_form.cleaned_data['coef0'],
        random_state = svc_form.cleaned_data['random_state']
    )
    df = get_preprocessed_df(user)
    X_train,X_test, y_train,y_test = split_data(df)
    svc.fit(X_train, y_train)
    y_pred = svc.predict(X_test)
    return compute_metrics(y_test, y_pred)

def rfc(rfc_form,user):
    rfc = RandomForestClassifier(
        n_estimators = rfc_form.cleaned_data['n_estimators'],
        criterion=rfc_form.cleaned_data['criterion'],
        max_depth=rfc_form.cleaned_data['max_depth'],
        min_samples_split=rfc_form.cleaned_data['min_samples_split'],
        min_samples_leaf=rfc_form.cleaned_data['min_samples_leaf'],
        max_features=rfc_form.cleaned_data['max_features'],
        random_state=rfc_form.cleaned_data['random_state']
    )
    df = get_preprocessed_df(user)
    X_train,X_test, y_train,y_test = split_data(df)
    rfc.fit(X_train, y_train)
    y_pred = rfc.predict(X_test)
    return compute_metrics(y_test, y_pred)

def km(km_form,user):
    km = KMeans(
        n_clusters=4,
        init = km_form.cleaned_data['init'],
        n_init=km_form.cleaned_data['n_init'],
        random_state=km_form.cleaned_data['random_state']
    )
    df = get_preprocessed_df(user)
    X = df[['weekly_study_time', 'absences', 'average_grade', 'behavior']]
    clusters = km.fit_predict(X)
    passed = df['final_outcome']
    markers = {0: 'o', 1: 's'}
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
        
    plt.figure(figsize=(16,12))

    for passed_val in [0, 1]:
        idx = passed == passed_val
        plt.scatter(
            X_pca[idx, 0],
            X_pca[idx, 1], 
            c=clusters[idx],
            cmap='viridis', 
            marker=markers[passed_val],
            label='Passed' if passed_val == 1 else 'Not Passed',
            edgecolor='k',
            alpha=0.7
        )
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.title('Clustering done using KMeans on weekly_study_time,absences,average_grade,behavior, reduced to 2D with PCA')
    plt.legend()
    cbar = plt.colorbar(label='Cluster label')
    cbar.set_ticks(range(len(set(clusters))))
    cbar.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return image_base64
