"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
import asyncio

def print_volume_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass


def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")
dispatcher = dispatcher.Dispatcher()
dispatcher.set_default_handler(default_handler)

client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
server = osc_server.BlockingOSCUDPServer(("127.0.0.1", 5006), dispatcher)

prefix = "../../data/"
suffix = "/.bin"
buffer_size = 10
sampling_freq = 2000

num_channels = 8
folder_name = "testing/unplugged"
num_seconds = 10

filepath = prefix + folder_name + suffix
num_samples = sampling_freq*num_seconds
for i in range(1):
	client.send_message("/recording_params", [num_samples, num_channels, buffer_size, filepath])
	print([num_samples, num_channels, buffer_size])
	msg = server.handle_request() # blocks to recieve message

client.send_message("/stop", 1)


# basic recording script

# - give the session a one-word descriptor
# - go into a trial loop waiting for a key press
# - key pressed, bonsai records for some fixed length
# - python waits for finish
# - return to idle
# - if stop key is pressed, 