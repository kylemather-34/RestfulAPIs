from http import HTTPStatus
from io import BytesIO

from fastapi import FastAPI, HTTPException, Request, Response
from PIL import Image

app = FastAPI()

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB


@app.post('/resize')
async def resize(width: int, height: int, request: Request):
    size = int(request.headers.get('Content-Length', 0))
    if not size:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='missing content-length header',
        )
    if size > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='image too large (max is 5MB)',
        )

    if width <= 0 or height <= 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='width and height must be positive',
        )

    data = await request.body()
    io = BytesIO(data)
    img = Image.open(io)
    img = img.resize((width, height))
    out = BytesIO()
    img.save(out, format='PNG')
    return Response(
        content=out.getvalue(),
        status_code=HTTPStatus.OK,
        media_type='image/png',
    )
