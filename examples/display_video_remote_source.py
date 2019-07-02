import sys
sys.path.append("../")
import asyncio

from cfv.functions import video_source, video_display_sink
from cfv.net.remote_port import RemoteOutPort
import logging

async def run():
  source = video_source.VideoSource("../../vehicle_detection_haarcascades/dataset/video2.avi")
  op_source = RemoteOutPort("127.0.0.1", 8000)
  source.add_outgoing_port(op_source)

  await op_source.setup()
  await source.run_async()

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