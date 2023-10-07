import pickle
import numpy as np
import pandas as pd

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "prediction": None}
    )


@app.post("/predict/")
def predict(request: Request):
    # Use your machine learning model here to make predictions
    # Replace this with your actual model code
    ## Load the model
    data = None
    regmodel = pickle.load(open("data\\regmodel.pkl", "rb"))
    scalar = pickle.load(open("data\\scaling.pkl", "rb"))
    print(data)

    new_data = scalar.transform(np.array(list(data.values())).reshape(1, -1))
    predicted_price = regmodel.predict(new_data)[0]

    return templates.TemplateResponse(
        "index.html", {"request": request, "prediction": predicted_price}
    )
