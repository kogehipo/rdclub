from machine import Pin, PWM
import utime

# BLE用の設定
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
BLE_NAME = "RD_TOHO"
ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble, name=BLE_NAME )

GPIO_SPEAKER = 4  # スピーカー
SPEAKER = PWM(Pin(GPIO_SPEAKER, Pin.OUT)) # スピーカー

GPIO_SPEAKER = 4  # スピーカー
GPIO_RED     = 2  # 各色のLED
GPIO_BLUE    = 3
GPIO_YELLOW  = 5
GPIO_GREEN   = 6
GPIO_BLUE2   = 7
GPIO_YELLOW2 = 8
GPIO_GREEN2  = 9
GPIO_RED2    = 10
RED     = Pin(GPIO_RED,     Pin.OUT) # LED
BLUE    = Pin(GPIO_BLUE,    Pin.OUT)
YELLOW  = Pin(GPIO_YELLOW,  Pin.OUT)
GREEN   = Pin(GPIO_GREEN,   Pin.OUT)
BLUE2   = Pin(GPIO_BLUE2,   Pin.OUT)
YELLOW2 = Pin(GPIO_YELLOW2, Pin.OUT)
GREEN2  = Pin(GPIO_GREEN2,  Pin.OUT)
RED2    = Pin(GPIO_RED2,    Pin.OUT)

# 使用する音を定義（ピタゴラスイッチは低いラ～高いドまでの音を使う）
# dict型でキーは音のID、値は音の属性 リスト
# 属性の内容は周波数、光らせるLED の色
tone = {
    "//": [   0.000, 0      ],  # 無音（休符）
    
    "C4" : [ 261.626, RED    ],  # C4
    "C4#": [ 277.183, RED2   ],  # C4s
    "D4" : [ 293.665, YELLOW ],  # D4
    "D4#": [ 311.127, YELLOW2],  # D4s
    "E4" : [ 329.628, GREEN  ],  # E4
    "F4" : [ 349.228, BLUE   ],  # F4
    "F4#": [ 369.994, BLUE2  ],  # F4s
    "G4" : [ 391.995, GREEN  ],  # G4
    "G4#": [ 415.305, GREEN2 ],  # G4s
    "A4" : [ 440.000, RED    ],  # A4
    "A4#": [ 466.164, RED2   ],  # A4s
    "B4" : [ 493.883, BLUE   ],  # B4

    "C5" : [ 523.251, YELLOW ],  # C5
    "C5#": [ 554.365, YELLOW2],  # C5s
    "D5" : [ 587.330, GREEN  ],  # D5
    "D5#": [ 622.254, GREEN2 ],  # D5s
    "E5" : [ 659.255, BLUE   ],  # E5
    "F5" : [ 698.456, GREEN2 ],  # F5
    "F5#": [ 739.989, GREEN2 ],  # F5s
    "G5" : [ 783.991, RED    ],  # G5
    "G5#": [ 830.609, RED2   ],  # G5s
    "A5" : [ 880.000, BLUE   ],  # A5
    "A5#": [ 932.328, BLUE2  ],  # A5s
    "B5" : [ 987.767, YELLOW ],  # B5

    "C6" : [ 1046.502, GREEN  ],  # C6
    "C6#": [ 1108.731, GREEN2 ],  # C6s
    "D6" : [ 1174.659, BLUE   ],  # D6
    "D6#": [ 1244.508, BLUE2  ],  # D6s
    "E6" : [ 1318.510, GREEN  ],  # E6
    "F6" : [ 1396.913, RED    ],  # F6
    "F6#": [ 1479.978, RED2   ],  # F6s
    "G6" : [ 1567.982, YELLOW ],  # G6
    "G6#": [ 1661.219, YELLOW ],  # G6s
    "A6" : [ 1760.000, GREEN  ],  # A6
    "A6#": [ 1864.655, GREEN2 ],  # A6s
    "B6" : [ 1975.533, BLUE   ],  # B6
}

# 音を鳴らす
def make_sound(data):
    if data == "//": # 無音（休符）の場合
        SPEAKER.duty_u16(0) # PWMのDutyを0とすることで波形は出力されずLOWとなり、音は出ない
        return

    try:
        SPEAKER.freq(int(tone[data][0] + 0.5)) # PWMの周波数を次のメロディー音の周波数に変更する。整数で渡す必要があるので、+0.5してから小数点以下切り捨て（thanks @naohiro2g）
        SPEAKER.duty_u16(0x8000) # PWMのDutyを50％に戻し、音を出す。Dutyは0～0xFFFFつまり65535までの間の値で設定
    except Exception as e:
        print(f"Error trapped: {e}")
 
# BLEからの入力値を処理する関数
def on_rx( data ):
    print( f"Received Data: {data}" )
    key = data.decode()  # バイト列を文字列に変換
    if len(key) > 2 and key[2] == 'S':
        key = key[0:3]
    else:
        key = key[0:2]
    print(key)
    make_sound(key)  # 音を出す

while True:
    # BLEから入力があれば処理関数に投げる
    if sp.is_connected():
        sp.on_write( on_rx )
