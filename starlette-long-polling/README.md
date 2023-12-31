This folder contains code to examine how the `is_disconnected` method in
Starlette can be used to detect when a request is cancelled, in a long-polling
scenario.

1. Create a Python virtual environment and install the dependencies
2. Run the server in a terminal with `uvicorn server:app`: the root of this app
   simulates a message that becomes available after several seconds.
3. Run the client with `python clientclose.py`, this client sends a web request
   to the server and closes the connection after 1 second
4. Wait for 5 seconds to see if the server prints the message
   "The client is no more connected!"
5. Open the page in web browsers and refresh the page to inspect how
   `is_disconnected()` returns true in such case.

## Test with Hypercorn

```bash
hypercorn server:app
```

## Results

1. Starlette with uvicorn always handle properly disconnections, detecting both
   scenarios in a web browser, when the user refreshes or closes the browser tab,
   and when a client closes the connection (see `clientclose.py` example).
   Requests appear as disconnected in these cases.
2. Starlette and Hypecorn instead do not work properly: they fail to detect when
   the browser tab or a client connection are closed while a request is being
   handled in the following scenario:

```python

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
```

However, Starlette and Hypercorn start working if the `is_disconnected()`
method (and therefore the ASGI `receive` function) are used more than once!

If we change the code above this way:

```diff

async def homepage(request: Request):
    # simulate a message that becomes available after 5 seconds...
    print("Received a request...")
    await asyncio.sleep(5)
+    await request.is_disconnected()
    if await request.is_disconnected():
        print("The client is no more connected!")
        return JSONResponse({"hello": "No more connected!"})
    else:
        print("All Good - still connected!")
    print("Returning a response...")
    return JSONResponse({"hello": "world"})
```

Then the code starts working also with Hypercorn.
