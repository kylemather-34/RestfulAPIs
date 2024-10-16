"""Write a handler to query logs.
The handler accept the following query parameters:
- offset (default to 0)
- count (default to 100)

    GET /logs?offset=10&count=20

If should use db.query_logs to get the logs and return them as a JSON response in the
following format:
{
    "count": <count>,
    "offset": <offset>,
    "logs": [
        {"level": "INFO", "time": "2024-01-01T00:00:00", "message": "Log message #0000"},
        {"level": "WARNING", "time": "2024-01-01T00:00:12.345000", "message": "Log message #0001"},
        ...
    ]
}

If the HTTP header `Accept` is set to `text/csv`, the handler should return the logs in
CSV format:
    level,time,message
    INFO,2024-01-01T00:00:00,Log message #0000
    WARNING,2024-01-01T00:00:12.345000,Log message #0001
    ...

If now logs matches the query, return a 404 (NOT_FOUND) response.
Don't forget to validate everything.

"""

import csv
from datetime import datetime
from http import HTTPStatus
from io import StringIO

from fastapi import FastAPI, Request, Response
from pydantic import BaseModel

import db

app = FastAPI()


class Log(BaseModel):
    level: str
    time: datetime
    message: str


class LogsResponse(BaseModel):
    count: int
    offset: int
    logs: list[Log]


@app.get('/logs')
def query_logs(req: Request, count: int = 100, offset: int = 0):
    if count < 1 or offset < 0:
        return Response(
            status_code=HTTPStatus.BAD_REQUEST,
            content='bad count or offset',
        )
    mime_type = req.headers.get('Accept', 'application/json')
    if mime_type == '*/*':
        mime_type = 'application/json'
    if mime_type not in {'application/json', 'text/csv'}:
        return Response(
            status_code=HTTPStatus.BAD_REQUEST,
            content='bad Accept',
        )

    records = list(db.query_logs(offset, count))
    if not records:
        return Response(status_code=HTTPStatus.NOT_FOUND)

    fn = json_response if mime_type == 'application/json' else csv_response
    return fn(records, offset)


def json_response(records: list[dict], offset: int) -> LogsResponse:
    logs = [Log(**r) for r in records]

    return LogsResponse(count=len(records), offset=offset, logs=logs)


def csv_response(logs: list[dict], _: int) -> Response:
    io = StringIO()
    writer = csv.DictWriter(io, fieldnames=['time', 'level', 'message'])
    writer.writeheader()
    writer.writerows(
        {
            'time': log['time'].isoformat(),
            'level': log['level'],
            'message': log['message'],
        }
        for log in logs
    )

    return Response(content=io.getvalue(), media_type='text/csv')
