from litestar import Litestar, get

from routes import spotify_route


@get('/')
async def index() -> str:
    return 'Hello, world!'


app = Litestar([index, spotify_route])
