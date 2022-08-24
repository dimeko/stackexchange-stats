#!/usr/bin/env python3

# This package is just a CLI entry point for development
# in order not to execute the ./stats/cmd/cmd.py every time
import sys

try:
   import stats.cmd.cmd as cmd
except KeyboardInterrupt:
      print('Interrupted before loading modules')
      sys.exit(0)

def main():
   cmd.run()

if __name__ == "__main__":
   try:
      main()
   except KeyboardInterrupt:
      print('Interrupted')
      sys.exit(0)