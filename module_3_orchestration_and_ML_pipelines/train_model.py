import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

import mlflow
import joblib
import pickle
import os
import prefect
from prefect import flow, task


mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("nyc-taxi-experiment")

@task
def read_data(data):
    df = pd.read_parquet(data)
    return df

@task
def data_process(df, categorical):
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)]

    df[categorical] = df[categorical].astype(str)

    return df

@task
def model_train(df,categorical):
        
        mlflow.sklearn.autolog()

        with mlflow.start_run():

            # df = pd.read_parquet(data)

            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)

            df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
            df.duration = df.duration.dt.total_seconds() / 60

            df = df[(df.duration >= 1) & (df.duration <= 60)]

            # categorical = ['PULocationID', 'DOLocationID']
            df[categorical] = df[categorical].astype(str)
        
            train_dicts = df[categorical].to_dict(orient='records')

            dv = DictVectorizer()
            X_train = dv.fit_transform(train_dicts)
            y_train = df['duration'].values

            lr = LinearRegression()
            lr.fit(X_train, y_train)

            y_train_pred = lr.predict(X_train)
            rmse = mean_squared_error(y_train, y_train_pred, squared=False)
            mlflow.log_metric("rmse", rmse)

            with open("models/model.b", "wb") as mod:
                pickle.dump(lr, mod)

            mlflow.log_artifact("models/lr.pkl", artifact_path="model")

            mlflow.sklearn.log_model(lr, artifact_path="models_mlflow")

        return lr

@flow
def main():
    os.makedirs('models', exist_ok=True)
    data='https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet'
    df=read_data(data)
    categorical = ['PULocationID', 'DOLocationID']
    df1=data_process(df, categorical)
    
    model_train(df1, categorical)

    model= os.path.getsize('models/model.b')

    print(f'size model b: {model}')
     
if __name__== "__main__":
    main()
    


    

