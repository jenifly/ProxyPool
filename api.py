from aiohttp import web
from db import conn


async def get_proxy(request):
    return web.Response(text=str(conn.pop()))


async def get_counts(request):
    return web.Response(text=str(conn.queue_len))


def run():
    app = web.Application()
    app.add_routes([web.get('/get', get_proxy), web.get('/count', get_counts)])
    web.run_app(app, port=2345)


if __name__ == "__main__":
    run()
