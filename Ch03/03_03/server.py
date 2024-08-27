import logging
from typing import Annotated
from http import HTTPStatus

from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S',
)


@app.post('/survey')
def survey(
    name: Annotated[str, Form()],
    happy: Annotated[str, Form()],
    talk: Annotated[str, Form()],
):
    logging.info('[survey] name: %r, happy: %r, talk: %r', name, happy, talk)
    return RedirectResponse(
        url='/static/thanks.html',
        status_code=HTTPStatus.FOUND,
    )
