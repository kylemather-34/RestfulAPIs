from fastapi import FastAPI

app = FastAPI()


@app.get('/health')
def health():
    # TODO: Add more health checks
    return {'error': None}


if __name__ == '__main__':
    from argparse import ArgumentParser

    import uvicorn
    from config import settings

    parser = ArgumentParser()
    parser.add_argument('--port', type=int, default=settings.port)
    args = parser.parse_args()

    settings.update(vars(args))

    if settings.port < 0 or settings.port > 65_535:
        raise SystemExit(f'error: invalid port - {settings.port}')

    uvicorn.run(app, port=settings.port)
