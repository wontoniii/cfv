import sys
sys.path.append("../")
import asyncio

from cfv.functions import video_source, video_display_sink
from cfv.net.remote_port import RemoteOutPort
import logging

async def run():
  tasks = []
  source = video_source.VideoSource("data/chaplin.mp4")
  op_source = RemoteOutPort("127.0.0.1", 8000)
  source.add_outgoing_port(op_source)
  await op_source.setup()

  tasks.extend(op_source.get_runners())
  tasks.append(asyncio.create_task(source.run_async()))
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