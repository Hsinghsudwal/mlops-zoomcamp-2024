# Setup

## Step 1: Overview of Workflow Deployment

* From Notebook Experiments to Production.
```
note.ipynb -> script.py
```

## Step 2: Setting Up Your Environment

```
1. conda create -n "venv" python=3.11 -y
2. conda activate venv
```

## Step 3: Install Requirements

```
pip install -r requirements.txt
```

## Step 4: The Script

```
python train_model.py
```
## Step 5: Prefect UI
```
prefect server start
```

## Step 6: Deployment
```
prefect deployment build train_model.py:main -n prefect-mlflow
```
* output: yaml file 

### server
```
prefect deployment apply main-deployment.yaml
```

## Step 7: Deployment agent
```
prefect agent start -q 'default'
```


