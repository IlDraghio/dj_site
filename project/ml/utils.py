from dataset.models import Data
import pandas as pd
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
    columns = ['behavior','F_outcome']
    for c in columns:
        le = LabelEncoder()
        df[c] = le.fit_transform(df[c])
        encoders[c] = le 
    return df, encoders

def one_hot_labels(df):
    ohe = OneHotEncoder(sparse=False, drop='first')
    encoded_data = ohe.fit_transform(df["gender"])
    encoded_cols = ohe.get_feature_names_out("gender")
    df_encoded = pd.DataFrame(encoded_data, columns=encoded_cols)
    df_final = pd.concat([df.drop(columns="gender"), df_encoded], axis=1)
    return df_final,ohe

def normalize_data(df):
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    scaler = StandardScaler()
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])
    return df,scaler

def split_data(df):
    X = df.drop(columns=["F_outcome"])
    y = df["F_outcome"]
    X_train,X_test, y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)
    return X_train,X_test, y_train,y_test

#will be only for downloading
"""
from datetime import datetime
import os
def save_to_csv(df,username):
    filename = f"{username}_preprocessedData_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.csv"
    folder = "media" 
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    df.to_csv(filepath, index=False, encoding="utf-8")
""" 