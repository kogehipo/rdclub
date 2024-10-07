from machine import Pin, PWM, Timer
import utime


# 外部設置したスイッチ
TactSw = Pin(21, machine.Pin.IN, machine.Pin.PULL_DOWN)


# BLE用の設定
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
BLE_NAME = "RD_TOHO"
ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble, name=BLE_NAME )


# スピーカー
sound_enabled = True
if sound_enabled:
    GPIO_SPEAKER = 28
    SPEAKER = PWM(Pin(GPIO_SPEAKER, Pin.OUT))


# LED
GPIO_RED     = 3
GPIO_BLUE    = 7
GPIO_YELLOW  = 10
GPIO_GREEN   = 6
GPIO_BLUE2   = 15
GPIO_YELLOW2 = 14
GPIO_GREEN2  = 11
GPIO_RED2    = 2
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

# LEDを消しておく
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
servo_enabled = True

def move_servo(servo, position):
    if position == 0:
        servo_pin[servo].duty_u16(angle[servo][0])
    else:
        servo_pin[servo].duty_u16(angle[servo][1])
    return

if servo_enabled:
    duty_max = 65535
    servo_pin = [ PWM(Pin(20, Pin.OUT)),
                  PWM(Pin(19, Pin.OUT)),
                  PWM(Pin(18, Pin.OUT)) ]
    angle = [[int(0.062 * duty_max), int(0.105 * duty_max)],
             [int(0.060 * duty_max), int(0.100 * duty_max)],
             [int(0.062 * duty_max), int(0.100 * duty_max)]]

    servo_pin[0].freq(50)
    servo_pin[1].freq(50)
    servo_pin[2].freq(50)

    move_servo(0,0)  # 反応しない
    move_servo(1,0)
    move_servo(2,0)
    duck = 0b000


# 使用する音を定義（ピタゴラスイッチは低いラ～高いドまでの音を使う）
# dict型でキーは音のID
# 値は  周波数、点灯するLED色、起きるアヒル
# アヒルは3bitでそれぞれの状態を示す
tone = {
    "//" : [   0.000, 0       , 0b000],  # 無音（休符）
    
    "C4" : [ 261.626, RED     , 0b100],  # C4   # C4はドの音で赤LEDを光らせる
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

    "C5" : [ 523.251, YELLOW  , 0b100],  # C5
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

    "C6" : [ 1046.502, GREEN  , 0b100],  # C6
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


# bps = 6.4 # 原曲128bpm / 60秒 = 2.1333...bps * 3連符 = 6.4bps
mspb = 156 # 6.4bpsの逆数 = 0.156ms　これが8分3連符ひとつ分の音の長さ、音の間隔となる

# ピタゴラスイッチのメロディーを配列で作成。
# 1要素が8分3連符ひとつ分の音の長さになる。 ""は無音（休符）
melody = [ "D5" ,"E5" ,""  ,"D5","E5" ,"",
           "G5" ,"F5#",""  ,"D5","E5" ,"",
           "D5" ,"E5" ,""  ,"D5","E5" ,"",
           "C6" ,"B5" ,""  ,"G5","A5" ,"",
           "D5" ,"E5" ,""  ,"D5","E5" ,"",
           "G5" ,"F5#",""  ,"D5","E5" ,"",
           "B4" ,"A4" ,""  ,"B4","C5" ,"",
           "C5#","D5" ,""  ,""  ,"D5" ,"",
           "D5" ,"E5" ,""  ,"D5","E5" ,"",
           "G5" ,"F5#",""  ,"D5","E5" ,"",
           "D5" ,"E5" ,""  ,"D5","E5" ,"",
           "C6" ,"B5" ,""  ,"G5","A5" ,"",
           "D5" ,"E5" ,""  ,"D5","E5" ,"",
           "G5" ,"F5#",""  ,"D5","E5" ,"",
           "B4" ,"A4" ,"A4","A4","A4" ,"A4",
           "A4" ,"A4" ,"A4","A4",""   ,"",
           "F5" ,"E5" ,""  ,"E5","F5#","E5",
           "F5#","G5" ,"G5","G5","D5" ,"",
           "B4" ,"C5" ,""  ,"C5","D5" ,"C5#",
           "D5" ,"B4" ,"B4","B4",""   ,"",
           "D5" ,"E5" ,""  ,"D5","E5" ,"",
           "G5" ,"F5#",""  ,"D5","E5" ,"",
           "D5" ,"E5" ,""  ,"D5","E5" ,"",
           "G5" ,"F5#",""  ,"D5","E5" ,"",
           "D5" ,"E5" ,""  ,"D5","E5" ,"",
           "C6" ,"B5" ,""  ,""  ,"G5" ,"",
           ""   ,""   ,""  ,""  ,""   ,"",
           ""   ,""   ,""  ,""  ,""   ,"",
           "D5" ,"E5" ,""  ,"D5","E5" ,"",
           "C6" ,"B5" ,""  ,""  ,"G5" ,"",
           ""   ,""   ,""  ,""  ,""   ,"",
           ""   ,""   ,""  ,""  ,""   ,"" ]

# カウンター
i = 0

# 音を鳴らすためのコールバック関数
def beat(timer):
    global melody
    global i
    global SPEAKER

    if i >= len(melody): # メロディーを最後まで演奏し終えたら
        #SPEAKER.deinit() # スピーカーのPWMを破棄して
        #turn_off_all_led() # LEDを消して
        timer.deinit() # タイマーを破棄して終了

    elif melody[i] == "": # メロディー音が0、つまり無音（休符）の場合
        SPEAKER.duty_u16(0) # PWMのDutyを0とすることで波形は出力されずLOWとなり、音は出ない
        turn_off_all_led() # LEDを消す

    else:
        SPEAKER.freq(int(tone[melody[i]][0] + 0.5)) # PWMの周波数を次のメロディー音の周波数に変更する。整数で渡す必要があるので、+0.5してから小数点以下切り捨て（thanks @naohiro2g）
        SPEAKER.duty_u16(0x8000) # PWMのDutyを50％に戻し、音を出す。Dutyは0～0xFFFFつまり65535までの間の値で設定
        #tone[melody[i]][1].value(1) # LEDを光らせる
        action(melody[i])

    i += 1 # メロディーを次に進めて終わり


# 装置を動かす
def  action(data):
    global tape
    global duck

    print("Sound data: $data")

    if sound_enabled:
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
    tone[data][1].value(1)   # あやしい！！！

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

    if servo_enabled:
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
    

key = ""     # 入力されたキー
sw = False   # スイッチの状態

# BLEからの入力値を処理する関数
def on_rx( data ):
    global key
    #print( f"Received Data: {data}" )
    key = data.decode()  # バイト列を文字列に変換
    if len(key) > 2 and key[2] == '#':
        key = key[0:3]
    else:
        key = key[0:2]
    print(key)
    action(key)


# 入力を待つ
while True:
    # BLEから入力があればコールバック関数が呼ばれる
    if sp.is_connected():
        sp.on_write( on_rx )

    if TactSw.value() == 1:
        if sw == False:
            print("SW is pressed.")
            sw = True

            # 8分3連符の間隔でコールバックを呼ぶタイマーを作成し、メロディースタート
            tim = Timer()
            tim.init(period=mspb, mode=Timer.PERIODIC, callback=beat)

    elif TactSw.value() == 0:
        if sw == True:
            print("SW is released.")
            sw = False

