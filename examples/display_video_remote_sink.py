import sys
sys.path.append("../")
import asyncio

from cfv.functions import video_sink
from cfv.net.remote_port import RemoteInPort
import logging

async def run():
  tasks = []
  sink = video_sink.VideoSink()
  ip_sink = RemoteInPort(sink.push_async, "127.0.0.1", 8000)
  sink.add_incoming_port(ip_sink)
  await ip_sink.setup()

  tasks.extend(ip_sink.get_runners())
  tasks.append(asyncio.create_task(sink.run_async()))
  await asyncio.gather(*tasks)

def main():
  logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
  )
  asyncio.run(run())

if __name__ == "__main__":
  main()