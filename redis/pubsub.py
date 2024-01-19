"""
Pub/Sub example with async Redis client.
"""
import asyncio

import redis.asyncio as redis

STOPWORD = "STOP"


async def reader(channel: redis.client.PubSub):  # type: ignore
    while True:
        message = await channel.get_message(ignore_subscribe_messages=True)
        if message is not None:
            print(f"(Reader) Message Received: {message}")
            if message["data"].decode() == STOPWORD:
                print("(Reader) STOP")
                break


async def main():
    client = redis.from_url("redis://localhost")
    async with client.pubsub() as pubsub:
        await pubsub.subscribe("channel:1", "channel:2")

        future = asyncio.create_task(reader(pubsub))

        await client.publish("channel:1", "Hello")
        await client.publish("channel:2", "World")
        await client.publish("channel:1", STOPWORD)

        await future


asyncio.run(main())
