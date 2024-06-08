import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader



@data_loader
def read_data(data):
    df=pd.read_parquet(data)

    return df



url='https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet'
read_data(url)