import json
import asyncio
from fastapi import FastAPI
from fastapi import Request
from fastapi import WebSocket

from fastapi.templating import Jinja2Templates

from fastapi.staticfiles import StaticFiles

import random

app = FastAPI()


app.mount("/static",StaticFiles(directory='static'))
templates = Jinja2Templates(directory="templates")


with open('measurements.json', 'r') as file:
    measurements = iter(json.loads(file.read()))


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.htm", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(0.1)
        payload = next(measurements)
        await websocket.send_json(payload)