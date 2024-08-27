"""Write an /info handler that will return a JSON object with:

- version: string, say "0.1.0"
- time: the current time in ISO format
- user: The user running the application (hint: os.getlogin)
"""

from datetime import datetime
from os import getlogin

from fastapi import FastAPI

app = FastAPI()


@app.get('/info')
def info():
    return {
        'version': '0.1.0',
        'time': datetime.now(),
        'user': getlogin(),
    }
