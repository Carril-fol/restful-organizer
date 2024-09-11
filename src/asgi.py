import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

def start_server(app):
    asyncio.run(serve(app, Config()))
