from fastapi import FastAPI, Request, HTTPException
from PIL import Image
from io import BytesIO
from http import HTTPStatus

app = FastAPI()

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB


@app.post('/size')
async def size(request: Request):
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

    data = await request.body()
    io = BytesIO(data)
    img = Image.open(io)
    return {'width': img.width, 'height': img.height}
