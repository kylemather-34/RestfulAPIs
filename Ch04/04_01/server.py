from datetime import datetime, timedelta

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class TimeResponse(BaseModel):
    delta: timedelta


@app.get('/time_delta')
def time_diff(start: datetime, end: datetime) -> TimeResponse:
    delta = end - start
    return TimeResponse(delta=delta)
