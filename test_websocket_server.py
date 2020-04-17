import asyncio
import sys

from cfv.net.websocket import WebSocketServer

import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
  )

async def main():
  server = WebSocketServer('127.0.0.1', 8080, None)
  await server.setup()
  print("Ready to run")
  await asyncio.gather(*server.get_runners())

if __name__== "__main__":
  asyncio.run(main())