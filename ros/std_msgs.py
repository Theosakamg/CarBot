#!/usr/bin/env python3

from ros.builtin_msgs import time

class Header(object):
  seq : int
  stamp : time
  frame_id : str

  def __init__(self):
    self.seq = 0
    self.stamp = time()
    self.frame_id = ""

class Time(object):
  data : time

  def __init__(self):
    self.data = time()
