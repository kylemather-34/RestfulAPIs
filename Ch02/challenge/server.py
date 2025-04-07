"""Write an /info handler that will return a JSON object with:

- version: string, say "0.1.0"
- time: the current time in ISO format
- user: The user running the application (hint: USER environment variable)
"""

from datetime import datetime, UTC
from os import environ # used for environment variable

from fastapi import FastAPI

app = FastAPI()


@app.get('/info')
def info():
    return {
        'version': '0.1.0',
        'time': datetime.now(tz=UTC), # returning current datetime in UTC format
        'user': environ['USER'], # user environment variable
    }
