import logging
from contextlib import asynccontextmanager
import time
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

# logging
loglevel = logging.DEBUG
logging.basicConfig(format="[%(asctime)s] %(levelname)s: %(message)s", level=loglevel)
logger = logging.getLogger(__name__)


# pydantic schemas
class PredictionRequest(BaseModel):
    text: str


class PredictionResponse(BaseModel):
    input: str
    result: List[dict]


# global model instance
MODEL = None


@asynccontextmanager
async def setup_teardown(app: FastAPI):
    """Handle loading model in/out of memory at app startup/shutdown."""
    start = time.time()
    global MODEL
    MODEL = pipeline(model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
    end = time.time()
    elapsed_secs = end - start
    logging.debug(
        "loaded pipeline in {:.3f} secs -- MODEL={}".format(elapsed_secs, MODEL)
    )
    yield
    MODEL = None


app = FastAPI(lifespan=setup_teardown)


@app.get("/healthcheck")
async def healthcheck() -> dict:
    return {"status": "ok"}


@app.post("/predict")
def predict(request: PredictionRequest) -> PredictionResponse:
    if MODEL is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    try:
        start = time.time()
        results = MODEL(request.text)
        end = time.time()
        elapsed_secs = end - start
        logging.debug(
            'inference: {:.3f} secs -- in="{}" -- out={}'.format(
                elapsed_secs, request.text, results
            )
        )
        return PredictionResponse(input=request.text, result=results)
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")
