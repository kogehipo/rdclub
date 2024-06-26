from machine import Pin, PWM
import utime

# LEDの接続情報
led_pin = [2,3,5,6,7,8,9,10]
led = []
for i in range(8):
    led.append(Pin(led_pin[i], Pin.OUT))

# ブザーの接続と音程
buzzer = PWM(Pin(4))
freqs = [262,293,329,349,392,440,493,523]



while True:
    for tone in range(8):
        led[tone].value(1)			# LEDオン
        buzzer.freq(freqs[tone])	# ブザーの音程
        buzzer.duty_u16(12000)		# ブザーを有効化
        utime.sleep(0.5)
        buzzer.duty_u16(0)			# ブザーを無効化
        led[tone].value(0)			# LED オフ
