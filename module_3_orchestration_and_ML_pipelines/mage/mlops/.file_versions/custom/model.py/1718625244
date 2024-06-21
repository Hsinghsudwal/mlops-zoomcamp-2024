if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom



@custom
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here
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

        return dv, ir
    
