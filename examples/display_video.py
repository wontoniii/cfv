import sys
sys.path.append("../")

from cfv.functions import video_source, video_display_sink
from cfv.net.port import LocalInPort, LocalOutPort
import logging

def run():
  sink = video_display_sink.VideoSink()
  ip_sink = LocalInPort(sink.push)
  sink.add_incoming_port(ip_sink)

  source = video_source.VideoSource("data/video2.avi")
  op_source = LocalOutPort(ip_sink)
  source.add_outgoing_port(op_source)
  source.run()

def main():
  logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
  )
  run()

if __name__ == "__main__":
  main()