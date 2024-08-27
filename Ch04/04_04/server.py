from fastapi import FastAPI

app = FastAPI()


class FreqError(Exception):
    pass


def char_freq(text: str):
    if not text:
        raise FreqError('empty text')

    freqs = {}
    for c in text.lower():
        freqs[c] = freqs.get(c, 0) + 1
    return freqs


@app.get('/freq')
def freq(text: str):
    return char_freq(text)
