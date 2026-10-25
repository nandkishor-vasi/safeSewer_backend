import os
import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
DATABASE_URL = os.environ.get("DATABASE_URL")

class Telemetry(BaseModel):
    mq135: float
    mq7: float
    dist: float
    lat: float
    lng: float

@app.post("/ingest")
def ingest_data(data: Telemetry):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO telemetry (mq135, mq7, distance, lat, lng) VALUES (%s, %s, %s, %s, %s)",
        (data.mq135, data.mq7, data.dist, data.lat, data.lng)
    )
    conn.commit()
    conn.close()
    return {"status": "success"}