from machine import Pin, PWM
import utime


# BLE用の設定
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
BLE_NAME = "RD_TOHO"
ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble, name=BLE_NAME )


# スピーカー
GPIO_SPEAKER = 4
SPEAKER = PWM(Pin(GPIO_SPEAKER, Pin.OUT))


# LED
GPIO_RED     = 2
GPIO_BLUE    = 3
GPIO_YELLOW  = 5
GPIO_GREEN   = 6
GPIO_BLUE2   = 7
GPIO_YELLOW2 = 8
GPIO_GREEN2  = 9
GPIO_RED2    = 10
RED     = Pin(GPIO_RED,     Pin.OUT)
BLUE    = Pin(GPIO_BLUE,    Pin.OUT)
YELLOW  = Pin(GPIO_YELLOW,  Pin.OUT)
GREEN   = Pin(GPIO_GREEN,   Pin.OUT)
BLUE2   = Pin(GPIO_BLUE2,   Pin.OUT)
YELLOW2 = Pin(GPIO_YELLOW2, Pin.OUT)
GREEN2  = Pin(GPIO_GREEN2,  Pin.OUT)
RED2    = Pin(GPIO_RED2,    Pin.OUT)

# 全部のLEDを消す
def turn_off_all_led():
    RED.value(0)
    BLUE.value(0)
    YELLOW.value(0)
    GREEN.value(0)
    RED2.value(0)
    BLUE2.value(0)
    YELLOW2.value(0)
    GREEN2.value(0)

turn_off_all_led()


# LEDテープ
GPIO_TAPE_BLUE  = 27
GPIO_TAPE_RED   = 26
GPIO_TAPE_WHITE = 22
TAPE_BLUE  = Pin(GPIO_TAPE_BLUE,  Pin.OUT)
TAPE_RED   = Pin(GPIO_TAPE_RED,   Pin.OUT)
TAPE_WHITE = Pin(GPIO_TAPE_WHITE, Pin.OUT)
TAPE_BLUE.value(1)  # 初期状態は消灯
TAPE_RED.value(1)
TAPE_WHITE.value(1)
tape = 0  # 点灯状態を制御する変数


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
    if position == 0:
        servo_pin[servo].duty_u16(angle[servo][0])
    else:
        servo_pin[servo].duty_u16(angle[servo][1])
    return

move_servo(0,0)
move_servo(1,0)
move_servo(2,0)
duck = 0b000

# 使用する音を定義（ピタゴラスイッチは低いラ～高いドまでの音を使う）
# dict型でキーは音のID
# 値は  周波数、点灯するLED色、起きるアヒル
# アヒルは3bitでそれぞれの状態を示す
tone = {
    "//" : [   0.000, 0       , 0b000],  # 無音（休符）
    
    "C4" : [ 261.626, RED     , 0b011],  # C4   # C4はドの音で赤LEDを光らせる
    "C4#": [ 277.183, RED2    , 0b010],  # C4#  # 以下同様
    "D4" : [ 293.665, YELLOW  , 0b001],  # D4
    "D4#": [ 311.127, YELLOW2 , 0b100],  # D4#
    "E4" : [ 329.628, GREEN   , 0b010],  # E4
    "F4" : [ 349.228, BLUE    , 0b001],  # F4
    "F4#": [ 369.994, BLUE2   , 0b101],  # F4#
    "G4" : [ 391.995, GREEN   , 0b011],  # G4
    "G4#": [ 415.305, GREEN2  , 0b110],  # G4#
    "A4" : [ 440.000, RED     , 0b010],  # A4
    "A4#": [ 466.164, RED2    , 0b001],  # A4#
    "B4" : [ 493.883, BLUE    , 0b101],  # B4

    "C5" : [ 523.251, YELLOW  , 0b011],  # C5
    "C5#": [ 554.365, YELLOW2 , 0b010],  # C5#
    "D5" : [ 587.330, GREEN   , 0b001],  # D5
    "D5#": [ 622.254, GREEN2  , 0b100],  # D5#
    "E5" : [ 659.255, BLUE    , 0b010],  # E5
    "F5" : [ 698.456, GREEN2  , 0b001],  # F5
    "F5#": [ 739.989, GREEN2  , 0b101],  # F5#
    "G5" : [ 783.991, RED     , 0b011],  # G5
    "G5#": [ 830.609, RED2    , 0b110],  # G5#
    "A5" : [ 880.000, BLUE    , 0b010],  # A5
    "A5#": [ 932.328, BLUE2   , 0b001],  # A5#
    "B5" : [ 987.767, YELLOW  , 0b101],  # B5

    "C6" : [ 1046.502, GREEN  , 0b011],  # C6
    "C6#": [ 1108.731, GREEN2 , 0b010],  # C6#
    "D6" : [ 1174.659, BLUE   , 0b001],  # D6
    "D6#": [ 1244.508, BLUE2  , 0b100],  # D6#
    "E6" : [ 1318.510, GREEN  , 0b010],  # E6
    "F6" : [ 1396.913, RED    , 0b001],  # F6
    "F6#": [ 1479.978, RED2   , 0b101],  # F6#
    "G6" : [ 1567.982, YELLOW , 0b011],  # G6
    "G6#": [ 1661.219, YELLOW , 0b110],  # G6#
    "A6" : [ 1760.000, GREEN  , 0b010],  # A6
    "A6#": [ 1864.655, GREEN2 , 0b001],  # A6#
    "B6" : [ 1975.533, BLUE   , 0b101],  # B6
}


# 装置を動かす
def  action(data):
    global tape
    global duck
    
    if data == "//": # 無音（休符）の場合
        SPEAKER.duty_u16(0) # PWMのDutyを0とすることで波形は出力されずLOWとなり、音は出ない
        return

    try:
        SPEAKER.freq(int(tone[data][0] + 0.5)) # PWMの周波数を次のメロディー音の周波数に変更する。整数で渡す必要があるので、+0.5してから小数点以下切り捨て（thanks @naohiro2g）
        SPEAKER.duty_u16(0x8000) # PWMのDutyを50％に戻し、音を出す。Dutyは0～0xFFFFつまり65535までの間の値で設定
    except Exception as e:
        print(f"Error trapped: {e}")

    # 音に応じたLEDだけを点灯する
    turn_off_all_led()
    tone[data][1].value(1)

    # テープはいったん消灯
    TAPE_BLUE.value(1)
    TAPE_RED.value(1)
    TAPE_WHITE.value(1)

    # 制御変数に応じて点灯する
    if  tape == 0:   # 全点灯
        TAPE_BLUE.value(0)
        TAPE_RED.value(0)
        TAPE_WHITE.value(0)
    elif tape == 1:  # 青だけ
        TAPE_BLUE.value(0)
    elif tape == 2:  # 赤だけ
        TAPE_RED.value(0)
    elif tape == 3:  # 白だけ
        TAPE_WHITE.value(0)

    tape += 1
    if tape > 3:
        tape = 0

    if  (duck & 0b001) != (tone[data][2] & 0b001):
        move_servo(0, tone[data][2] & 0b001)
        duck &= 0b110
        duck |= tone[data][2] & 0b001

    if (duck & 0b010) != (tone[data][2] & 0b010):
        move_servo(1, tone[data][2] & 0b010)
        duck &= 0b101
        duck |= tone[data][2] & 0b010

    if (duck & 0b100) != (tone[data][2] & 0b100):
        move_servo(2, tone[data][2] & 0b100)
        duck &= 0b011
        duck |= tone[data][2] & 0b100


# BLEからの入力値を処理する関数
def on_rx( data ):
    print( f"Received Data: {data}" )
    key = data.decode()  # バイト列を文字列に変換
    if len(key) > 2 and key[2] == '#':
        key = key[0:3]
    else:
        key = key[0:2]
    print(key)
    action(key)


while True:
    # BLEから入力があればコールバック関数が呼ばれる
    if sp.is_connected():
        sp.on_write( on_rx )
