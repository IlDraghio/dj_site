from django.contrib.auth.models import User
from dataset.models import Data
from .models import Preprocessed_data
import pandas as pd
import csv
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

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
    X = df.drop(columns=["F_outcome"])
    y = df["F_outcome"]
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

