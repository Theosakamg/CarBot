#!/usr/bin/env python3

from .std_msgs import Header

class Vector3(object):
  x : float
  y : float
  z : float

  def __init__(self):
    self.x = 0.0
    self.y = 0.0
    self.z = 0.0

class Twist(object):
  linear : Vector3
  angular : Vector3

  def __init__(self):
    self.linear = Vector3()
    self.angular = Vector3()

class Transform(object):
  translation : Vector3
  rotation : Quaternion

  def __init__(self):
    self.translation = Vector3()
    self.rotation = Quaternion()

class TransformStamped(object):
  header : Header
  child_frame_id : str  # the frame id of the child frame
  transform : Transform

  def __init__(self):
    self.header = Header()
    self.child_frame_id = ""
    self.transform = Transform()

class TwistStamped(object):
  header : Header
  twist : Twist

  def __init__(self):
    self.header = Header()
    self.twist = Twist()

class Point(object):
  x : float
  y : float
  z : float

  def __init__(self):
    self.x = 0.0
    self.y = 0.0
    self.z = 0.0

class Quaternion(object):
  x : float
  y : float
  z : float
  w : float

  def __init__(self):
    self.x = 0.0
    self.y = 0.0
    self.z = 0.0
    self.w = 0.0

class QuaternionStamped(object):
  header : Header
  quaternion : Quaternion

  def __init__(self):
    self.header = Header()
    self.quaternion = Quaternion()

class Pose(object):
  position : Point
  orientation : Quaternion

  def __init__(self):
    self.position = Point()
    self.orientation = Quaternion()

class PoseStamped(object):
  header : Header
  pose : Pose

  def __init__(self):
    self.header = Header()
    self.pose = Pose()
