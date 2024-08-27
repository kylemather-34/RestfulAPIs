from fastapi import FastAPI

app = FastAPI()


@app.get('/health')
def health():
    # TODO: Add more health checks
    return {'error': None}


if __name__ == '__main__':
    from config import settings
    import uvicorn

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--port', type=int, default=settings.port)
    args = parser.parse_args()

    settings.update(vars(args))

    uvicorn.run(app, port=settings.port)
