import time
import pigpio

import argparse
parser = argparse.ArgumentParser()
#parser.add_argument('--example', nargs='?', const=1, type=int, default=3)
parser.add_argument('freq', type=float, default=1000.0, nargs='?', \
                    help='PWM frequency')
args = parser.parse_args()
print('args: %s' % args)

pwm_pin = 17

#connect to pigpiod daemon
pi = pigpio.pi()

# setup pin as an output
pi.set_mode(pwm_pin, pigpio.OUTPUT)


# pi set frequency
freq = args.freq# from command line optional positional argument
pi.set_PWM_frequency(pwm_pin, freq)
pi.set_PWM_range(pwm_pin, 100)

dc = 50# 50% duty cycle
pi.set_PWM_dutycycle(pwm_pin,dc)
time.sleep(30.0)

#cleanup
pi.set_PWM_dutycycle(pwm_pin,0)
pi.set_mode(pwm_pin, pigpio.INPUT)

#disconnect
pi.stop()
