#!/usr/bin/python3.7

import asyncio
import argparse
import sys
import logging
from cfv.manager.local_manager import LocalManager

def main():
  parser = argparse.ArgumentParser(description='Execute video analytics processing pipeline.')
  parser.add_argument('config', metavar='config', type=str, help='pipeline configuration file')

  args = vars(parser.parse_args())
  logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
  )

  local_manager = LocalManager()
  local_manager.process_config_json(args["config"])
  asyncio.run(local_manager.start())


if __name__== "__main__":
  main()