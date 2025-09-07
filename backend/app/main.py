from fastapi import FastAPI, Request
from .i18n import get_message

app = FastAPI()


@app.get("/hello")
async def hello(request: Request):
    lang = request.headers.get("Accept-Language", "en")
    return {"message": get_message("greeting", lang)}
