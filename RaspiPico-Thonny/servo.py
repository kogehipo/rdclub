from machine import PWM, Pin
import utime

# サーボモーター
duty_max = 65535
servo_pin = [PWM(Pin(16)), PWM(Pin(17)), PWM(Pin(18))]
angle = [[int(0.060 * duty_max), int(0.100 * duty_max)],
         [int(0.055 * duty_max), int(0.095 * duty_max)],
         [int(0.060 * duty_max), int(0.100 * duty_max)]]
servo_pin[0].freq(50)
servo_pin[1].freq(50)
servo_pin[2].freq(50)

def move_servo(servo, position):
    servo_pin[servo].duty_u16(angle[servo][position])
    return

# 最初に90度の位置に移動
move_servo(0, 0)
move_servo(1, 0)
move_servo(2, 0)

utime.sleep(2)
move_servo(0, 1)
utime.sleep(2)
move_servo(1, 1)
utime.sleep(2)
move_servo(2, 1)
