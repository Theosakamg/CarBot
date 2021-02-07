#!/usr/bin/python3
from picar.SunFounder_TB6612 import TB6612
from drivers import PCA9685
from components import Servo, Throttle
import decimal
import time

GPIO_MOTOR_ROT_A = 17
GPIO_MOTOR_ROT_B = 27

CHN_PWM_DIR = 0
CHN_PWM_A = 4
CHN_PWM_B = 5

DIR_MIN = 30
DIR_MAX = 150

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
  # direction()
  engine()


def direction():
  delay = 1.0/80
  tempo = 5

  print("Start !")
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

  throttle_a = Throttle.Throttle(CHN_PWM_A)
  throttle_a.debug = True
  throttle_b = Throttle.Throttle(CHN_PWM_B)
  throttle_b.debug = True

  left_wheel = TB6612.Motor(GPIO_MOTOR_ROT_A, pwm=throttle_a, offset=False)
  right_wheel = TB6612.Motor(GPIO_MOTOR_ROT_B, pwm=throttle_b, offset=False)




if __name__ == "__main__":
    main()