import numpy as np
from sklearn.utils.sparsefuncs import inplace_column_scale
from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.constant.training_pipeline import SAVED_MODEL_DIR, SCHEMA_DROP_COLS, SCHEMA_FILE_PATH
from sensor.exception import SensorException
from sensor.logger import logging
import os,sys
from sensor.ml.model.estimator import ModelResolver, TargetValueMapping
from sensor.pipeline.training_pipeline import TrainPipeline
from sensor.constant.application import APP_HOST, APP_PORT
from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from sensor.ml.model.estimator import ModelResolver, TargetValueMapping
from sensor.utils.main_utils import load_object, read_yaml_file
from uvicorn import run as app_run

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainPipeline()
        if train_pipeline.is_pipeline_running:
            return Response('Training pipeline is already running')
        train_pipeline.run_pipeline()
    except Exception as e:
        return Response(f'Error occured! {e}')

import pandas as pd

@app.post("/predict")
async def predict_route(file: UploadFile = File(...)):
    try:
        # Read the CSV file into a Pandas DataFrame
        df = pd.read_csv(file.file, na_values = 'na')
        df.replace({'na':np.nan}, inplace=True)
        _schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        df = df.drop(_schema_config[SCHEMA_DROP_COLS],axis=1)
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response('Model is not available')
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
        
        # Return the DataFrame as a JSON response
        response = df.to_json(orient="records")

        return response

    except Exception as e:
        print(SensorException(e,sys))
        return Response(f'Error occured! {e}')

def main():
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)

if __name__ == '__main__':
    app_run(app,host=APP_HOST, port=APP_PORT)