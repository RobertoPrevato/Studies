import asyncio

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route


async def homepage(request: Request):
    # simulate a message that becomes available after 5 seconds...
    print("Received a request...")
    await asyncio.sleep(5)

    if await request.is_disconnected():
        print("The client is no more connected!")
        return JSONResponse({"hello": "No more connected!"})
    else:
        print("All Good - still connected!")
    print("Returning a response...")
    return JSONResponse({"hello": "world"})


app = Starlette(
    debug=True,
    routes=[
        Route("/", homepage),
    ],
)
