import sys
sys.path.append("../")

from cfv.functions import video_source, video_display_sink, car_detection
from cfv.net.local_port import LocalInPort, LocalInPortAsync, LocalOutPort, LocalOutPortAsync
import asyncio
import logging
import argparse

def run():
  sink = video_display_sink.VideoSink()
  ip_sink = LocalInPort(sink.push)
  sink.add_incoming_port(ip_sink)

  cd = car_detection.CarDetection("data/cars.xml")
  op_cd = LocalOutPort(ip_sink)
  cd.add_outgoing_port(op_cd)
  ip_cd = LocalInPort(cd.push)
  cd.add_incoming_port(ip_cd)

  source = video_source.VideoSource("data/video2.avi")
  op_source = LocalOutPort(ip_cd)
  source.add_outgoing_port(op_source)
  source.run()


async def run_async():
  tasks = []
  sink = video_display_sink.VideoSink()
  ip_sink = LocalInPortAsync(sink.push_async)
  sink.add_incoming_port(ip_sink)
  to_add = sink.get_async_tasks()
  if len(to_add) > 0:
    tasks.extend(to_add)

  cd = car_detection.CarDetection("data/cars.xml")
  op_cd = LocalOutPortAsync(ip_sink)
  cd.add_outgoing_port(op_cd)
  ip_cd = LocalInPortAsync(cd.push_async)
  cd.add_incoming_port(ip_cd)
  to_add = cd.get_async_tasks()
  if len(to_add) > 0:
    tasks.extend(to_add)

  source = video_source.VideoSource("data/video2.avi")
  op_source = LocalOutPortAsync(ip_cd)
  source.add_outgoing_port(op_source)
  tasks.append(asyncio.create_task(source.run_async()))

  await asyncio.gather(*tasks)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-a', '--async', action='store_true',
                      help="run asynchronously")

  args = vars(parser.parse_args())
  logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
  )
  if not args["async"]:
    run()
  else:
    asyncio.run(run_async())

if __name__ == "__main__":
  main()