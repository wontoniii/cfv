import sys
sys.path.append("../")

from cfv.functions import video_source, video_display_sink, car_detection
from cfv.net.port import LocalInPort, LocalInPortAsync, LocalOutPort, LocalOutPortAsync
import asyncio
import logging

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


def run_async():
  sink = video_display_sink.VideoSink()
  sink.add_incoming_port(None)

def main():
  logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
  )
  if True:
    run()
  else:
    run_async()

if __name__ == "__main__":
  main()