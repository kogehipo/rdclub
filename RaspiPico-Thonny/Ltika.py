from machine import Pin
import utime
# PicoではGPIO25にLEDが接続されている
led = Pin('LED', Pin.OUT)
while True:
    # LEDの状態を反転(点滅)
    led.toggle()
    # 200ms waitする
    utime.sleep_ms(200)