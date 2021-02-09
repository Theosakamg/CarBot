#!/usr/bin/env python3

# Drivers
from picar.SunFounder_TB6612 import TB6612
from drivers import PCA9685
from components import Servo, Throttle

# ROS
from ros.geometry_msgs import Twist

# System
import threading
import time

GPIO_MOTOR_ROT_A = 17
GPIO_MOTOR_ROT_B = 27

CHN_PWM_DIR = 0
CHN_PWM_A = 4
CHN_PWM_B = 5

DIR_MIN = 30
DIR_MAX = 150

class CarNode(object):
  vel = Twist()
  freq = 50
  is_running = True

  def __init__(self):

    # Initialize Direction
    self.servo = Servo.Servo(CHN_PWM_DIR)
    self.servo.debug = True
    self.servo.min_degree_value = DIR_MIN
    self.servo.max_degree_value = DIR_MAX
    self.servo.offset = 15

    # Initialize engine
    self.throttle_a = Throttle.Throttle(CHN_PWM_A)
    self.throttle_a.debug = True
    self.throttle_b = Throttle.Throttle(CHN_PWM_B)
    self.throttle_b.debug = True

    self.motorA = TB6612.Motor(GPIO_MOTOR_ROT_A, pwm=self.throttle_a.write, offset=False)
    self.motorB = TB6612.Motor(GPIO_MOTOR_ROT_B, pwm=self.throttle_b.write, offset=False)

    # Set origin
    self.servo.default()
    self.motorA.speed = 0
    self.motorB.speed = 0

    # Start main loop
    self.thread = threading.Thread(target=self.__loop, args=())
    self.thread.start()

  def __loop(self):
    while(self.is_running):
      # Manage Direction

      # Manage Engine
      if (self.vel.linear.x > 0):
        self.motorA.forward()
        self.motorB.forward()
      else:
        self.motorA.backward()
        self.motorB.backward()
    
      speed = abs(self.vel.linear.x)

      if (speed > 1.0):
        motorSpeed = 100
      else:
        motorSpeed = 100 * speed

      self.motorA.speed = motorSpeed
      self.motorB.speed = motorSpeed

      time.sleep(1/self.freq)

  def publish(self, vel : Twist):
    self.vel.linear.x = vel.linear.x
    self.vel.linear.y = vel.linear.y   # Not use for car !
    self.vel.linear.z = vel.linear.z   # Not use for car !

    self.vel.angular.x = vel.angular.x
    self.vel.angular.y = vel.angular.y
    self.vel.angular.z = vel.angular.z

  def emergency(self):
    self.vel = Twist()
    self.is_running = False
    self.motorA.speed = 0
    self.motorB.speed = 0
