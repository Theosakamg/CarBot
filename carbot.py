#!/usr/bin/env python3

from picar.SunFounder_TB6612 import TB6612
from drivers import PCA9685
from components import Servo, Throttle
from ros.geometry_msgs import Twist

import atexit
import decimal
import time

GPIO_MOTOR_ROT_A = 17
GPIO_MOTOR_ROT_B = 27

CHN_PWM_DIR = 0
CHN_PWM_A = 4
CHN_PWM_B = 5

DIR_MIN = 30
DIR_MAX = 150

tempo = 5

node = CarNode()

def float_range(A, L=None, D=None):
  #Use float number in range() function
  # if L and D argument is null set A=0.0 and D = 1.0
  if L == None:
    L = A + 0.0
    A = 0.0
  if D == None:
    D = 1.0
  while True:
    if D > 0 and A >= L:
      break
    elif D < 0 and A <= L:
      break
    yield (float(A)) # return float number
    A = A + D

def main():
  atexit.register(emergency)
  # direction()
  # engine()

  speed = 1.0
  distance = 2.0

  vel_msg = Twist()
  vel_msg.linear.x = speed

  #while not rospy.is_shutdown():
  #Setting the current time for distance calculus
  t0 = time.time()  # rospy.Time.now().to_sec()
  current_distance = 0

  #Loop to move the turtle in an specified distance
  while(current_distance < distance):
      #Publish the velocity
      node.publish(vel_msg)
      #Takes actual time to velocity calculus
      t1 = time.time()  # rospy.Time.now().to_sec()
      #Calculates distancePoseStamped
      current_distance= speed*(t1-t0)

  #After the loop, stops the robot
  vel_msg.linear.x = 0
  #Force the robot to stop
  node.publish(vel_msg)


def direction():
  delay = 1.0/80

  print("Start !")
  global servo
  servo = Servo.Servo(CHN_PWM_DIR)
  servo.debug = True
  #servo.driver.debug = True
  servo.min_degree_value = DIR_MIN
  servo.max_degree_value = DIR_MAX

  servo.default()
  time.sleep(tempo)

  print("Counter-clock...")
  for i in float_range(DIR_MAX, DIR_MIN, -1/3):
    servo.write(i)
    time.sleep(delay)
  time.sleep(tempo)

  print("Clock...")
  for i in float_range(DIR_MIN, DIR_MAX, 1/3):
    servo.write(i)
    time.sleep(delay)
  time.sleep(tempo)

  print("Limit/step...")
  servo.min()
  time.sleep(tempo)

  servo.default()
  time.sleep(tempo)

  servo.max()
  time.sleep(tempo)

  print("Halt.")
  servo.default()


def engine():
  delay = 0.05

  throttle_a = Throttle.Throttle(CHN_PWM_A)
  throttle_a.debug = True
  throttle_b = Throttle.Throttle(CHN_PWM_B)
  throttle_b.debug = True

  global motorA
  global motorB
  motorA = TB6612.Motor(GPIO_MOTOR_ROT_A, pwm=throttle_a.write, offset=False)
  motorB = TB6612.Motor(GPIO_MOTOR_ROT_B, pwm=throttle_b.write, offset=False)

  motorA.forward()
  for i in range(0, 101, 20):
    motorA.speed = i
    time.sleep(3)
  time.sleep(tempo)

  for i in range(100, -1, -1):
    motorA.speed = i
    time.sleep(delay)
  time.sleep(tempo)

  motorA.backward()
  for i in range(0, 101, 20):
    motorA.speed = i
    time.sleep(3)
  time.sleep(tempo)

  motorA.speed = 0
  motorA.forward()
  motorB.speed = 0
  motorB.forward()
  
  for i in range(0, 101, 10):
    motorA.speed = i
    motorB.speed = i
    time.sleep(1)

  motorA.speed = 0
  motorA.forward()
  motorB.speed = 0
  motorB.forward()

def emergency():
  # servo.default()
  # motorA.stop()
  # motorB.stop()
  node.emergency()

if __name__ == "__main__":
    main()